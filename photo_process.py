import torch
import torchvision.transforms as transforms
from efficientnet_pytorch import EfficientNet

from settings import (
    IMAGE_SIZE,
    LABELS_MAP,
    MODEL_NAME,
)


def photo_classifier(img) -> list[str]:
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

    model = EfficientNet.from_pretrained(MODEL_NAME).eval()
    with torch.no_grad():
        logits = model(img)

    predictions = torch.topk(logits, k=3).indices.squeeze(dim=0).tolist()
    top_answers = []
    for idx in predictions:
        label = LABELS_MAP[idx]
        prob = torch.softmax(logits, dim=1)[0, idx].item()
        top_answers.append('{:<75} ({:.2f}%)'.format(label, prob * 100))
    return top_answers
