import json
import os
import pickle
import platform
import subprocess as sp
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
from torch.nn import functional as F

from data import OFFENDER_CSV_PATH, OFFENDER_IMAGES_DIR, unmake_safe_name
from detection import detect_faces
from similarity import _tx, get_edge_model

OUT_DIR = Path.cwd() / "data" / "sshots"
EMBEDDINGS_PATH = Path.cwd() / "models" / "offender_embeddings.pkl"
TITLE_KEYWORD = "Photo Booth"  # Example keyword to identify target window
INTERVAL_SEC = 1/30  # 30 FPS
COMPARISON_THRESHHOLD = 70.0
OFFENDER_REGISTRY = pd.read_csv(OFFENDER_CSV_PATH)
IS_MACOS = platform.system() == "Darwin"

OUT_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    return sp.run(cmd, check=True, stdout=sp.PIPE, text=True).stdout


def find_target():
    if IS_MACOS:
        return find_target_macos()
    else:
        return find_target_linux()


def find_target_linux():
    raw = run(["hyprctl", "clients", "-j"])
    for c in json.loads(raw):
        if TITLE_KEYWORD.lower() in c.get("title", "").lower():
            x, y = c["at"][0], c["at"][1]
            w, h = c["size"][0], c["size"][1]
            return c["address"], f"{x},{y} {w}x{h}"
    return None, None


def find_target_macos():
    applescript = f'''
    tell application "System Events"
        repeat with proc in (every process whose background only is false)
            try
                repeat with win in (every window of proc)
                    if name of win contains "{TITLE_KEYWORD}" then
                        set winPos to position of win
                        set winSize to size of win
                        return (name of proc) & "|" & (name of win) & "|" & (item 1 of winPos) & "|" & (item 2 of winPos) & "|" & (item 1 of winSize) & "|" & (item 2 of winSize)
                    end if
                end repeat
            end try
        end repeat
        return ""
    end tell
    '''
    try:
        result = run(["osascript", "-e", applescript])
        result = result.strip()
        if not result:
            return None, None
        parts = result.split("|")
        if len(parts) >= 6:
            app_name, _, x, y, w, h = parts[:6]
            return app_name, f"{x},{y} {w}x{h}"
    except Exception as e:
        print(f"Error finding target window on macOS: {e}")
    return None, None


def focus_window(addr):
    if IS_MACOS:
        focus_window_macos(addr)
    else:
        focus_window_linux(addr)


def focus_window_linux(addr):
    sp.run(["hyprctl", "dispatch", "focuswindow", f"address:{addr}"], check=True)


def focus_window_macos(app_name):
    applescript = f'tell application "{app_name}" to activate'
    try:
        sp.run(["osascript", "-e", applescript], check=True)
    except Exception as e:
        print(f"Error focusing window on macOS: {e}")
        fallback_script = f'''
        tell application "System Events"
            repeat with proc in (every process whose background only is false)
                try
                    repeat with win in (every window of proc)
                        if name of win contains "{TITLE_KEYWORD}" then
                            tell proc to set frontmost to true
                            return
                        end if
                    end repeat
                end try
            end repeat
        end tell
        '''
        sp.run(["osascript", "-e", fallback_script], check=True)


def snap_once(geom: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_path = OUT_DIR / f"messenger_{ts}.png"
    if IS_MACOS:
        snap_once_macos(geom, out_path)
    else:
        snap_once_linux(geom, out_path)
    print(f"Saved screenshot to {out_path}")
    screenshots = sorted(OUT_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in screenshots[5:]:
        old.unlink()
    return out_path


def snap_once_linux(geom: str, out_path: Path):
    sp.run(["grim", "-g", geom, str(out_path)], check=True)


def snap_once_macos(geom: str, out_path: Path):
    pos_part, size_part = geom.split(" ")
    x, y = map(int, pos_part.split(","))
    w, h = map(int, size_part.split("x"))
    sp.run(["screencapture", "-R", f"{x},{y},{w},{h}", str(out_path)], check=True)


def compare_embeddings(embedding1, embedding2) -> float:
    """Computes cosine similarity between two embeddings."""
    embedding1 = torch.from_numpy(embedding1)
    embedding2 = torch.from_numpy(embedding2)
    similarity = F.cosine_similarity(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()
    return max(0, min(100, similarity * 100))


def find_match(
    img_fromstream: np.ndarray, offender_embeddings: dict[str, np.ndarray], model
) -> pd.Series | None:
    """Finds a matching offender from pre-computed embeddings."""
    device = next(model.parameters()).device
    with torch.no_grad():
        live_embedding = model(
            _tx(cv2.cvtColor(img_fromstream, cv2.COLOR_RGB2BGR))[None].to(device)
        )[0].cpu().numpy()

    for offender_filename, stored_embedding in offender_embeddings.items():
        similarity = compare_embeddings(live_embedding, stored_embedding)
        if similarity >= COMPARISON_THRESHHOLD:
            offender_name = unmake_safe_name(offender_filename)
            print(f"Found matching offender: {offender_name} with similarity {similarity:.2f}%")
            offender_row = OFFENDER_REGISTRY[OFFENDER_REGISTRY["Name"] == offender_name]
            if not offender_row.empty:
                return offender_row.iloc[0]
    print("No match found")
    return None


def main():
    try:
        if not EMBEDDINGS_PATH.is_file() or EMBEDDINGS_PATH.stat().st_size == 0:
            print(f"Warning: Offender embeddings not found at '{EMBEDDINGS_PATH}'.")
            print("Please run 'uv run src/precompute_embeddings.py' to generate them.")
            offender_embeddings = {}
        else:
            with open(EMBEDDINGS_PATH, "rb") as f:
                offender_embeddings = pickle.load(f)
            print(f"Loaded {len(offender_embeddings)} offender embeddings.")

        model = get_edge_model("edgeface_s_gamma_05")

        while True:
            addr, geom = find_target()
            if geom:
                focus_window(addr)
                screenshot_path = snap_once(geom)
                img = cv2.imread(str(screenshot_path))
                if img is None:
                    print(f"Failed to load image: {screenshot_path}")
                    continue
                faces = detect_faces(img)
                for i, face in enumerate(faces):
                    cv2.imshow(f"Face {i+1}", face)
                    cv2.waitKey(1)
                for face in faces:
                    offender = find_match(face, offender_embeddings, model)
                    if offender is not None:
                        print("Offender details:")
                        print(offender.to_string())
            else:
                print(f"Could not find window with title containing '{TITLE_KEYWORD}'")
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
