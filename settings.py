import json

# top secret, not for distribution
BOT_TOKEN = '5375646413:AAGI-xKBST6YJQyHKCfk6HIc7to05JmpquQ'
DEVELOPER_CHAT_ID = '675176359'

LABELS_PATH = './labels_map.json'
MODEL_NAME = 'efficientnet-b0'
IMAGE_SIZE = 224

with open(LABELS_PATH) as f:
    LABELS_MAP = {int(key): value for key, value in json.load(f).items()}
