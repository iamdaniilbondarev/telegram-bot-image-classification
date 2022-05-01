import json

# top secret, not for distribution
BASE_WIKI_URL = 'https://en.wikipedia.org/wiki/'
BOT_TOKEN = '5375646413:AAGI-xKBST6YJQyHKCfk6HIc7to05JmpquQ'

LABELS_PATH = './labels_map.json'
MODEL_NAME = 'efficientnet-b0'
IMAGE_SIZE = 224

with open(LABELS_PATH) as f:
    LABELS_MAP = {int(key): value for key, value in json.load(f).items()}
