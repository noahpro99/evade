from __future__ import annotations

import cv2
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from torchvision import transforms

_EDGE_MODEL_CACHE: dict[str, torch.nn.Module] = {}

model_configs = {
    "edgeface_base": {
        "repo": "idiap/EdgeFace-Base",
        "filename": "edgeface_base.pt",
        "timm_model": "edgenext_base",
        "post_setup": lambda x: x,
    },
    "edgeface_s_gamma_05": {
        "repo": "idiap/EdgeFace-S-GAMMA",
        "filename": "edgeface_s_gamma_05.pt",
        "timm_model": "edgenext_small",
        "post_setup": lambda x: replace_linear_with_lowrank_2(x, rank_ratio=0.5),
    },
    "edgeface_xs_gamma_06": {
        "repo": "idiap/EdgeFace-XS-GAMMA",
        "filename": "edgeface_xs_gamma_06.pt",
        "timm_model": "edgenext_x_small",
        "post_setup": lambda x: replace_linear_with_lowrank_2(x, rank_ratio=0.6),
    },
    "edgeface_xxs": {
        "repo": "idiap/EdgeFace-XXS",
        "filename": "edgeface_xxs.pt",
        "timm_model": "edgenext_xx_small",
        "post_setup": lambda x: x,
    },
}

# FIXED: proper preprocessing
_tx = transforms.Compose(
    [
        transforms.ToPILImage(),
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)


class LoRaLin(nn.Module):
    def __init__(self, in_features, out_features, rank, bias=True):
        super().__init__()
        self.linear1 = nn.Linear(in_features, rank, bias=False)
        self.linear2 = nn.Linear(rank, out_features, bias=bias)

    def forward(self, input):
        return self.linear2(self.linear1(input))


def replace_linear_with_lowrank_recursive_2(model, rank_ratio=0.2):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "head" not in name:
            in_features, out_features = module.in_features, module.out_features
            rank = max(2, int(min(in_features, out_features) * rank_ratio))
            bias = module.bias is not None
            setattr(model, name, LoRaLin(in_features, out_features, rank, bias))
        else:
            replace_linear_with_lowrank_recursive_2(module, rank_ratio)


def replace_linear_with_lowrank_2(model, rank_ratio=0.2):
    replace_linear_with_lowrank_recursive_2(model, rank_ratio)
    return model


class TimmFRWrapperV2(nn.Module):
    def __init__(self, model_name="edgenext_x_small", featdim=512, batchnorm=False):
        super().__init__()
        self.model = timm.create_model(model_name)
        self.model.reset_classifier(featdim)

    def forward(self, x):
        return self.model(x)


def get_edge_model(name: str) -> torch.nn.Module:
    if name in _EDGE_MODEL_CACHE:
        return _EDGE_MODEL_CACHE[name]

    if name not in model_configs:
        raise KeyError(f"Unknown edge model '{name}'")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cfg = model_configs[name]
    model_path = hf_hub_download(
        repo_id=cfg["repo"], filename=cfg["filename"], local_dir="models"
    )
    model = TimmFRWrapperV2(cfg["timm_model"])
    model = cfg["post_setup"](model)

    state = torch.load(model_path, map_location="cpu")
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing or unexpected:
        print(f"[warn] Missing: {missing} | Unexpected: {unexpected}")

    model.eval().to(device)
    _EDGE_MODEL_CACHE[name] = model
    return model


def compare(img_left, img_right, variant="edgeface_s_gamma_05") -> float:
    mdl = get_edge_model(variant)
    dev = next(mdl.parameters()).device
    with torch.no_grad():
        ea = mdl(_tx(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))[None].to(dev))[0]
        eb = mdl(_tx(cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB))[None].to(dev))[0]
    pct = float(F.cosine_similarity(ea[None], eb[None]).item() * 100)
    pct = max(0, min(100, pct))
    print(f"Similarity: {pct:.2f}%")
    return pct


# Threshold for face matching (percentage)
COMPARISON_THRESHOLD = 75.0  # 75% similarity threshold


def compare_embeddings(embedding1, embedding2) -> float:
    """Compare two face embeddings and return similarity percentage."""
    # Convert numpy arrays to torch tensors if needed
    if isinstance(embedding1, torch.Tensor):
        emb1 = embedding1
    else:
        emb1 = torch.from_numpy(embedding1)

    if isinstance(embedding2, torch.Tensor):
        emb2 = embedding2
    else:
        emb2 = torch.from_numpy(embedding2)

    # Compute cosine similarity and convert to percentage
    similarity = F.cosine_similarity(emb1[None], emb2[None]).item()
    pct = float(similarity * 100)
    pct = max(0, min(100, pct))
    return pct


def get_face_encodings(img_bgr, variant="edgeface_s_gamma_05"):
    """Extract face encodings from detected faces in an image."""
    from detection import detect_faces

    faces = detect_faces(img_bgr)
    if not faces:
        return []

    model = get_edge_model(variant)
    device = next(model.parameters()).device
    encodings = []

    with torch.no_grad():
        for face in faces:
            img_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            encoding = model(_tx(img_rgb)[None].to(device))[0].cpu().numpy()
            encodings.append(encoding)

    return encodings


def compare_faces(known_embeddings, face_encoding, tolerance=COMPARISON_THRESHOLD):
    """Compare a face encoding against known embeddings."""
    matches = []
    for known_embedding in known_embeddings:
        similarity = compare_embeddings(face_encoding, known_embedding)
        matches.append(similarity >= tolerance)
    return matches


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python similarity.py <image1> <image2>")
        sys.exit(1)

    img1_path = sys.argv[1]
    img2_path = sys.argv[2]

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("Error loading images.")
        sys.exit(1)

    result = compare(img1, img2)
    print(f"Final similarity: {result:.2f}%")
