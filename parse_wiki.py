import requests
from bs4 import BeautifulSoup

from settings import BASE_WIKI_URL


def prepare_wiki_url(key_word: str) -> str:
    key_word = key_word.split(',')[0].split(' ')
    key_word = '_'.join(key_word).capitalize()
    return BASE_WIKI_URL + key_word


def extract_first_paragraph(key_word: str) -> tuple[str, str]:
    """Extract paragraph from wiki article corresponding to key_word"""
    wiki_url = prepare_wiki_url(key_word)
    response = requests.get(wiki_url)
    soup = BeautifulSoup(response.text, features='html.parser')
    text = ''
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    return text.strip().split('\n')[0], wiki_url
