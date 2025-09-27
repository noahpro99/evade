import json
import os
import pickle
import platform
import subprocess as sp
import threading
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from data import OFFENDER_CSV_PATH, download_images_if_missing, OFFENDER_IMAGES_DIR, unmake_safe_name
from detection import detect_faces
from similarity import _tx, get_edge_model, COMPARISON_THRESHHOLD, compare_embeddings, get_face_encodings

OUT_DIR = Path.cwd() / "data" / "sshots"
EMBEDDINGS_PATH = Path.cwd() / "models" / "offender_embeddings.pkl"
TITLE_KEYWORD = "Photo Booth"  # Example keyword to identify target window
INTERVAL_SEC = 1.0
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


def save_image_async(image_data: np.ndarray, path: Path):
    """Saves image data to a file in a separate thread."""
    threading.Thread(target=cv2.imwrite, args=(str(path), image_data)).start()


def snap_once(geom: str) -> np.ndarray | None:
    """Captures a screenshot and returns the image data."""
    if IS_MACOS:
        return snap_once_macos(geom)
    else:
        return snap_once_linux(geom)


def snap_once_linux(geom: str) -> np.ndarray | None:
    try:
        output = sp.check_output(["grim", "-g", geom, "-"])
        img_np = np.frombuffer(output, np.uint8)
        return cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    except sp.CalledProcessError as e:
        print(f"Error capturing screenshot on Linux: {e}")
        return None


def snap_once_macos(geom: str) -> np.ndarray | None:
    import tempfile
    
    pos_part, size_part = geom.split(" ")
    x, y = map(int, pos_part.split(","))
    w, h = map(int, size_part.split("x"))
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        cmd = ["screencapture", "-R", f"{x},{y},{w},{h}", "-o", temp_path]
        
        result = sp.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ERROR: screencapture failed with return code {result.returncode}")
            print(f"stderr: {result.stderr}")
            return None
        
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            print("ERROR: Screenshot file is empty or was not created")
            return None
            
        decoded_img = cv2.imread(temp_path)
        if decoded_img is None:
            print("ERROR: Failed to load screenshot image")
            return None
            
        return decoded_img
        
    except Exception as e:
        print(f"Error capturing screenshot on macOS: {e}")
        return None
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def find_match(
    img_fromstream: np.ndarray, offender_embeddings: dict[str, np.ndarray], model
) -> pd.Series | None:
    device = next(model.parameters()).device
    with torch.no_grad():
        img_rgb = cv2.cvtColor(img_fromstream, cv2.COLOR_BGR2RGB)
        live_embedding = model(_tx(img_rgb)[None].to(device))[0].cpu().numpy()

    for offender_filename, stored_embedding in offender_embeddings.items():
        similarity = compare_embeddings(live_embedding, stored_embedding)
        if similarity >= COMPARISON_THRESHOLD:
            offender_name = unmake_safe_name(offender_filename)
            print(
                f"Found matching offender: {offender_name} with similarity {similarity:.2f}%"
            )
            offender_row = OFFENDER_REGISTRY[OFFENDER_REGISTRY["Name"] == offender_name]
            if not offender_row.empty:
                return offender_row.iloc[0]
    print("No match found")
    return None


def main():
    try:
        download_images_if_missing()
        if not EMBEDDINGS_PATH.is_file() or EMBEDDINGS_PATH.stat().st_size == 0:
            print(f"Warning: Offender embeddings not found at '{EMBEDDINGS_PATH}'.")
            print("Please run 'uv run src/precompute_embeddings.py' to generate them.")
            offender_embeddings = {}
        else:
            with open(EMBEDDINGS_PATH, "rb") as f:
                offender_embeddings = pickle.load(f)
            print(f"Loaded {len(offender_embeddings)} offender embeddings.")

        print(f"Starting monitoring for windows containing '{TITLE_KEYWORD}'...")
        print("Press Ctrl+C to stop.")
        
        while True:
            addr, geom = find_target()
            if geom:
                focus_window(addr)
                img_data = snap_once(geom)
                if img_data is not None:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    out_path = OUT_DIR / f"messenger_{ts}.png"
                    save_image_async(img_data, out_path)

                    # Detect faces in the image
                    faces = detect_faces(img_data)

                    if faces:
                        model = get_edge_model("edgeface_s_gamma_05")
                        for i, face in enumerate(faces):
                            cv2.imshow(f"Face {i+1}", face)
                            cv2.waitKey(1)
                            
                            offender = find_match(face, offender_embeddings, model)
                            if offender is not None:
                                print("Offender details:")
                                print(offender.to_string())
                else:
                    print("Failed to capture screenshot")
            else:
                print(f"Could not find window with title containing '{TITLE_KEYWORD}'")
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
