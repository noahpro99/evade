import json
import os
import subprocess as sp
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from data import OFFENDER_CSV_PATH, OFFENDER_IMAGES_DIR, unmake_safe_name
from detection import detect_faces
from similarity import compare

OUT_DIR = Path.cwd() / "data" / "sshots"
TITLE_KEYWORD = "Messenger call"
INTERVAL_SEC = 1.0
COMPARISON_THRESHHOLD = 70.0
OFFENDER_REGISTRY = pd.read_csv(OFFENDER_CSV_PATH)

OUT_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd):
    return sp.run(cmd, check=True, stdout=sp.PIPE, text=True).stdout


def find_target():
    raw = run(["hyprctl", "clients", "-j"])
    for c in json.loads(raw):
        if TITLE_KEYWORD.lower() in c.get("title", "").lower():
            # geometry: "x,y WxH"
            x, y = c["at"][0], c["at"][1]
            w, h = c["size"][0], c["size"][1]
            return c["address"], f"{x},{y} {w}x{h}"
    return None, None


def focus_window(addr):
    sp.run(["hyprctl", "dispatch", "focuswindow", f"address:{addr}"], check=True)


def snap_once(geom: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_path = OUT_DIR / f"messenger_{ts}.png"
    # grim is non-interactive with -g; avoids hyprshot pipeline
    sp.run(["grim", "-g", geom, str(out_path)], check=True)
    print(f"Saved screenshot to {out_path}")
    screenshots = sorted(
        OUT_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    for old in screenshots[5:]:
        old.unlink()
    return out_path


def find_match(img_fromstream: np.ndarray) -> pd.Series | None:
    offender_name = None
    for offender_filename in os.listdir(OFFENDER_IMAGES_DIR):
        offender_image = cv2.imread(
            os.path.join(OFFENDER_IMAGES_DIR, offender_filename)
        )
        if compare(offender_image, img_fromstream) >= COMPARISON_THRESHHOLD:
            offender_name = unmake_safe_name(offender_filename)
            print(f"Found matching offender: {offender_name}")
            break
    offender_row = OFFENDER_REGISTRY[OFFENDER_REGISTRY["Name"] == offender_name]
    if offender_row.empty:
        print("No match found")
        return None
    assert len(offender_row) == 1
    print(f"Match found: {offender_name}")
    return offender_row.iloc[0]


def main():
    try:
        while True:
            addr, geom = find_target()
            if geom:
                focus_window(addr)
                snap_once(geom)
                faces = detect_faces(
                    sorted(OUT_DIR.glob("*.png"), key=os.path.getmtime)[0]
                )
                for face in faces:
                    offender = find_match(face)
                    if offender is not None:
                        print("Offender details:")
                        print(offender.to_string())
            else:
                print(f"Could not find window with title containing '{TITLE_KEYWORD}'")
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
