import atexit
import subprocess
import sys

import numpy as np
import whisper

SRC_RATE = 48_000  # pw-record rate
TGT_RATE = 16_000  # Whisper expects 16 kHz
CH = 2  # desktop mix is stereo
SAMPWIDTH = 2  # s16
FRAMES = 4096  # pw-record chunk size (frames)
CHUNK_BYTES = FRAMES * CH * SAMPWIDTH
WINDOW_SEC = 5
CHUNKS_PER_WIN = (SRC_RATE * WINDOW_SEC) // FRAMES  # 48000/4096 * 5 ≈ 58

CMD = [
    "pw-record",
    "-P",
    "{ stream.capture.sink=true }",  # capture post-mix sink (desktop audio only)
    "--rate",
    str(SRC_RATE),
    "--channels",
    str(CH),
    "--format",
    "s16",
    "-",  # write raw PCM to stdout
]


def main():
    model = whisper.load_model("small")

    proc = subprocess.Popen(
        CMD,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=0,
    )
    if not proc.stdout:
        sys.exit("pw-record stdout unavailable")
    atexit.register(proc.kill)

    buf = []
    try:
        while True:
            chunk = proc.stdout.read(CHUNK_BYTES)
            if not chunk:
                break
            buf.append(chunk)
            if len(buf) >= CHUNKS_PER_WIN:
                block = b"".join(buf)
                buf.clear()

                # bytes -> int16 -> stereo to mono
                pcm = (
                    np.frombuffer(block, dtype=np.int16)
                    .reshape(-1, CH)
                    .mean(axis=1)
                    .astype(np.int16)
                )

                # int16 -> float32 in [-1, 1]
                mono = pcm.astype(np.float32) / 32768.0

                # 48 kHz -> 16 kHz (exact decimation by 3)
                audio = mono[:: (SRC_RATE // TGT_RATE)].copy()

                # transcribe and print only the text line
                text = model.transcribe(audio, fp16=False)["text"]
                if text:
                    print(text, flush=True)

    finally:
        proc.kill()
        proc.wait(timeout=1)


if __name__ == "__main__":
    main()
