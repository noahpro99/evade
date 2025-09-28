import os
import pickle
from pathlib import Path

import cv2
import torch

from similarity import _tx, get_edge_model
from detection import detect_faces  # Import the face detection function

OFFENDER_IMAGES_DIR = Path.cwd() / "data" / "offender_list" / "images"
EMBEDDINGS_PATH = Path.cwd() / "models" / "offender_embeddings.pkl"


def precompute_embeddings():
    model = get_edge_model("edgeface_s_gamma_05")
    device = next(model.parameters()).device

    embeddings = {}
    print("Generating embeddings from offender images...")
    for offender_filename in os.listdir(OFFENDER_IMAGES_DIR):
        if offender_filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(OFFENDER_IMAGES_DIR, offender_filename)
            image = cv2.imread(image_path)  
            if image is not None:
                faces = detect_faces(image)  
                if not faces:
                    print(f"WARNING: No face detected in {offender_filename}. Skipping.")
                    continue
                cropped_face = faces[0]
                img_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
                with torch.no_grad():
                    embedding = model(_tx(img_rgb)[None].to(device))[0]
                    embeddings[offender_filename] = embedding.cpu().numpy()

    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(embeddings, f)

    print(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_PATH}")


if __name__ == "__main__":
    precompute_embeddings()