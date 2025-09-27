from __future__ import annotations

import cv2
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from huggingface_hub import hf_hub_download
from torchvision import transforms

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

_tx = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
    ]
)


class LoRaLin(nn.Module):
    def __init__(self, in_features, out_features, rank, bias=True):
        super(LoRaLin, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.linear1 = nn.Linear(in_features, rank, bias=False)
        self.linear2 = nn.Linear(rank, out_features, bias=bias)

    def forward(self, input):
        x = self.linear1(input)
        x = self.linear2(x)
        return x


def replace_linear_with_lowrank_recursive_2(model, rank_ratio=0.2):
    for name, module in model.named_children():
        if isinstance(module, nn.Linear) and "head" not in name:
            in_features = module.in_features
            out_features = module.out_features
            rank = max(2, int(min(in_features, out_features) * rank_ratio))
            bias = False
            if module.bias is not None:
                bias = True
            lowrank_module = LoRaLin(in_features, out_features, rank, bias)

            setattr(model, name, lowrank_module)
        else:
            replace_linear_with_lowrank_recursive_2(module, rank_ratio)


def replace_linear_with_lowrank_2(model, rank_ratio=0.2):
    replace_linear_with_lowrank_recursive_2(model, rank_ratio)
    return model


class TimmFRWrapperV2(nn.Module):
    """
    Wraps timm model
    """

    def __init__(self, model_name="edgenext_x_small", featdim=512, batchnorm=False):
        super().__init__()
        self.featdim = featdim
        self.model_name = model_name

        self.model = timm.create_model(self.model_name)
        self.model.reset_classifier(self.featdim)

    def forward(self, x):
        x = self.model(x)
        return x


def get_edge_model(name: str) -> torch.nn.Module:
    if name not in get_edge_model.cache:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = hf_hub_download(
            repo_id=model_configs[name]["repo"],
            filename=model_configs[name]["filename"],
            local_dir="models",
        )
        model = TimmFRWrapperV2(model_configs[name]["timm_model"], batchnorm=False)
        model = model_configs[name]["post_setup"](model)
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model = model.eval()
        model.to(device)
        get_edge_model.cache[name] = model
    return get_edge_model.cache[name]


get_edge_model.cache = {}


def compare(img_left, img_right, variant="edgeface_s_gamma_05") -> float:
    mdl = get_edge_model(variant)
    dev = next(mdl.parameters()).device
    with torch.no_grad():
        ea = mdl(_tx(cv2.cvtColor(img_left, cv2.COLOR_RGB2BGR))[None].to(dev))[0]
        eb = mdl(_tx(cv2.cvtColor(img_right, cv2.COLOR_RGB2BGR))[None].to(dev))[0]
    pct = float(F.cosine_similarity(ea[None], eb[None]).item() * 100)
    pct = max(0, min(100, pct))
    print(f"Similarity: {pct:.2f}%")
    return pct


if __name__ == "__main__":
    import os

    # print device
    print("Using device:", "cuda" if torch.cuda.is_available() else "cpu")

    image_files = [
        os.path.join("data", "test_images", f)
        for f in os.listdir(os.path.join("data", "test_images"))
        if f.endswith(".png")
    ]
    image_files = sorted(image_files, key=os.path.getmtime, reverse=True)
    if len(image_files) < 2:
        print("Not enough images in data/test_images/")
        exit(1)
    image_path1 = image_files[0]
    image_path2 = image_files[1]
    image_array1 = cv2.imread(image_path1)
    image_array2 = cv2.imread(image_path2)
    print(compare(image_array1, image_array2, "edgeface_s_gamma_05"))
