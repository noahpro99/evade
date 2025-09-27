import json
import os
import platform
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
            # geometry: "x,y WxH"
            x, y = c["at"][0], c["at"][1]
            w, h = c["size"][0], c["size"][1]
            return c["address"], f"{x},{y} {w}x{h}"
    return None, None


def find_target_macos():
    # Use AppleScript to find windows with the target keyword
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
            
        # Parse the pipe-separated result
        parts = result.split("|")
        if len(parts) >= 6:
            app_name = parts[0]
            window_title = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            w = int(parts[4])
            h = int(parts[5])
            
            # Return app name as identifier and geometry
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
    # Focus the application using AppleScript
    applescript = f'''
    tell application "{app_name}" to activate
    '''
    try:
        sp.run(["osascript", "-e", applescript], check=True)
    except Exception as e:
        print(f"Error focusing window on macOS: {e}")
        # Fallback: try to activate any application containing the title keyword
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
    screenshots = sorted(
        OUT_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    for old in screenshots[5:]:
        old.unlink()
    return out_path


def snap_once_linux(geom: str, out_path: Path):
    # grim is non-interactive with -g; avoids hyprshot pipeline
    sp.run(["grim", "-g", geom, str(out_path)], check=True)


def snap_once_macos(geom: str, out_path: Path):
    # Parse geometry "x,y WxH"
    pos_part, size_part = geom.split(" ")
    x, y = map(int, pos_part.split(","))
    w, h = map(int, size_part.split("x"))
    
    # Use screencapture with region selection
    sp.run([
        "screencapture", 
        "-R", f"{x},{y},{w},{h}",  # Region: x,y,width,height
        str(out_path)
    ], check=True)


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
