import json

BASE_WIKI_URL = 'https://en.wikipedia.org/wiki/'
BOT_TOKEN = 'token'
LABELS_PATH = './labels_map.json'
MODEL_NAME = 'efficientnet-b0'
IMAGE_SIZE = 224

with open(LABELS_PATH) as f:
    LABELS_MAP = {int(key): value for key, value in json.load(f).items()}
