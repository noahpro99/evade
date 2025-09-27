from pathlib import Path
from urllib import request

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from numpy.typing import NDArray

_FACE_DETECTOR_INSTANCE = None
FACE_DETECTOR_MODEL_PATH = Path.cwd() / "models" / "detector.tflite"


def _get_face_detector():
    global _FACE_DETECTOR_INSTANCE
    if _FACE_DETECTOR_INSTANCE is None:
        if not FACE_DETECTOR_MODEL_PATH.is_file():
            print("Downloading face detector model...")
            FACE_DETECTOR_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            request.urlretrieve(
                "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite",
                str(FACE_DETECTOR_MODEL_PATH),
            )
        base_options = mp_python.BaseOptions(model_asset_path=FACE_DETECTOR_MODEL_PATH)
        options = mp_vision.FaceDetectorOptions(base_options=base_options)
        _FACE_DETECTOR_INSTANCE = mp_vision.FaceDetector.create_from_options(options)
    return _FACE_DETECTOR_INSTANCE


def detect_faces(image_path: Path) -> list[NDArray]:
    detector = _get_face_detector()
    if detector is None:
        return []
    mp_image = mp.Image.create_from_file(str(image_path))
    result = detector.detect(mp_image)
    if not result.detections:
        return []
    img_bgr = cv2.imread(str(image_path))
    if img_bgr is None:
        return []
    h, w, _ = img_bgr.shape
    faces: list[np.ndarray] = []
    for det in result.detections:
        box = det.bounding_box  # has origin_x, origin_y, width, height
        x1 = max(0, box.origin_x)
        y1 = max(0, box.origin_y)
        x2 = min(w, x1 + box.width)
        y2 = min(h, y1 + box.height)
        if x2 > x1 and y2 > y1:
            faces.append(img_bgr[y1:y2, x1:x2].copy())
    return faces


if __name__ == "__main__":
    import sys

    _get_face_detector()

    if len(sys.argv) != 2:
        print("Usage: python detection.py <image_path>")
        sys.exit(1)
    img_path = Path(sys.argv[1])
    if not img_path.is_file():
        print(f"File not found: {img_path}")
        sys.exit(1)
    faces = detect_faces(img_path)
    print(f"Detected {len(faces)} faces")
    for i, face in enumerate(faces):
        out_path = img_path.parent / f"{img_path.stem}_face_{i + 1}{img_path.suffix}"
        cv2.imwrite(str(out_path), face)
        print(f"Saved face {i + 1} to {out_path}")
