import torch
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet

from settings import (
    IMAGE_SIZE,
    LABELS_MAP,
    MODEL_NAME,
)

EFFICIENT_NET = EfficientNet.from_pretrained(MODEL_NAME).eval()


def photo_classifier(img) -> str:
    """Make model prediction"""
    trfms = transforms.Compose([
        transforms.Resize(IMAGE_SIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225],
        ),
    ])
    img = trfms(img).unsqueeze(dim=0)

    with torch.no_grad():
        model_response = EFFICIENT_NET(img)

    top_idx = torch.argmax(model_response).item()
    return LABELS_MAP[top_idx]
