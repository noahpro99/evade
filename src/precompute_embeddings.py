import os
import pickle
from pathlib import Path

import cv2
import torch
from similarity import get_edge_model, _tx

OFFENDER_IMAGES_DIR = Path.cwd() / "data" / "offender_list" / "images"
EMBEDDINGS_PATH = Path.cwd() / "models" / "offender_embeddings.pkl"

def precompute_embeddings():
    """Pre-computes embeddings for all offender images and saves them to a file."""
    model = get_edge_model("edgeface_s_gamma_05")
    device = next(model.parameters()).device
    
    embeddings = {}
    for offender_filename in os.listdir(OFFENDER_IMAGES_DIR):
        if offender_filename.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(OFFENDER_IMAGES_DIR, offender_filename)
            image = cv2.imread(image_path)
            if image is not None:
                with torch.no_grad():
                    embedding = model(_tx(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))[None].to(device))[0]
                    embeddings[offender_filename] = embedding.cpu().numpy()
    
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(embeddings, f)
    
    print(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_PATH}")

if __name__ == "__main__":
    precompute_embeddings()