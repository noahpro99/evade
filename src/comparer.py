from __future__ import annotations

from pathlib import Path
import cv2
import gradio as gr
import numpy as np
import torch
import torch.nn.functional as F
from torchvision import transforms
from huggingface_hub import hf_hub_download

from title import title_css, title_with_logo

from face_alignment import align
from PIL import Image
import net

model_configs = {
    "HyperFace-10k-LDM": {
        "repo": "idiap/HyperFace-10k-LDM",
        "filename": "HyperFace_10k_LDM.ckpt",
    },
    "HyperFace-10k-StyleGAN": {
        "repo": "idiap/HyperFace-10k-StyleGAN",
        "filename": "HyperFace_10k_StyleGAN.ckpt",
    },
    "HyperFace-50k-StyleGAN": {
        "repo": "idiap/HyperFace-50k-StyleGAN",
        "filename": "HyperFace_50k_StyleGAN.ckpt",
    },
}

DATA_DIR = Path("data")
EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
PRELOADED = sorted(p for p in DATA_DIR.iterdir() if p.suffix.lower() in EXTS)

HYPERFACE_MODELS = [
    "HyperFace-10k-LDM",
    "HyperFace-10k-StyleGAN",
    "HyperFace-50k-StyleGAN",
]

def to_input(pil_rgb_image):
    np_img = np.array(pil_rgb_image)
    brg_img = ((np_img[:,:,::-1] / 255.) - 0.5) / 0.5
    tensor = torch.tensor([brg_img.transpose(2,0,1)]).float()
    return tensor


def get_face_rec_model(name: str) -> torch.nn.Module:
    if name not in get_face_rec_model.cache:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model_path = hf_hub_download(
            repo_id=model_configs[name]["repo"],
            filename=model_configs[name]["filename"],
            local_dir="models",
        )

        model = net.build_model(model_name='ir_50')
        statedict = torch.load(model_path, map_location=device)['state_dict']
        model_statedict = {key[6:]:val for key, val in statedict.items() if key.startswith('model.')}
        model.load_state_dict(model_statedict)
        model.eval()
        model.to(device)
        
        get_face_rec_model.cache[name] = model
    return get_face_rec_model.cache[name]


get_face_rec_model.cache = {}

def compare(img_left, img_right, variant):

    img_left = Image.fromarray(img_left).convert('RGB')
    img_right = Image.fromarray(img_right).convert('RGB')

    mdl = get_face_rec_model(variant)
    dev = next(mdl.parameters()).device
    with torch.no_grad():
        ea = mdl(to_input(img_left).to(dev))[0]
        eb = mdl(to_input(img_right).to(dev))[0]
    pct = float(F.cosine_similarity(ea, eb).item() * 100)
    pct = max(0, min(100, pct))
    return img_left, img_right, pct
