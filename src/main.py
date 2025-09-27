#!/usr/bin/env python3
import json
import subprocess as sp
import time
from datetime import datetime
from pathlib import Path

OUT_DIR = Path.cwd() / "data" / "sshots"
TITLE_KEYWORD = "Messenger call"
INTERVAL_SEC = 1.0

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


def main():
    try:
        while True:
            addr, geom = find_target()
            if geom:
                focus_window(addr)
                snap_once(geom)
            time.sleep(INTERVAL_SEC)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
