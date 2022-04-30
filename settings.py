import json

# top secret, not for distribution
BOT_TOKEN = 'token'
DEVELOPER_CHAT_ID = "id"

LABELS_PATH = './labels_map.json'
MODEL_NAME = 'efficientnet-b0'
IMAGE_SIZE = 224

with open(LABELS_PATH) as f:
    LABELS_MAP = {int(key): value for key, value in json.load(f).items()}
