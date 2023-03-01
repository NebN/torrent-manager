import re
import urllib
from pathlib import Path
import json
import requests
from fuzzywuzzy import process, fuzz
from src.model import Category
import logging


BASE_API_URL = 'https://api.themoviedb.org/3/'
BASE_TELEGRAM_API_URL = 'https://api.telegram.org/bot'
LOGGER = logging.getLogger()
w
def _encode(string):
  return urllib.parse.quote(string.encode())


class MovieApi:
  def __init__(self, key) -> None:
    self.key = key


  def identify(self, name, category):
    search_url_term = 'movie' if category == Category.MOVIE else 'tv'
    title_label = 'title' if category == Category.MOVIE else 'name'
    url = f'{BASE_API_URL}search/{search_url_term}?query={_encode(name)}&api_key={self.key}'

    LOGGER.debug(f'GET {url}')

    resp = json.loads(requests.get(url).content)
    match = MovieApi._best_match(search_term=name, items=resp['results'], extract_term=lambda x: x[title_label])

    if category == Category.MOVIE:
      return MovieApi._movie(match, name)
    else:
      pass


  @staticmethod
  def _movie(dict, path):
    pass

  @staticmethod
  def _tv(dict, path):
    pass

  
  @staticmethod
  def _best_match(search_term, items, extract_term):
    terms = [extract_term(item) for item in items]

    LOGGER.info(process.extract(search_term, terms, scorer=fuzz.token_sort_ratio))

    match = process.extractOne(search_term, terms)
    for item in items:
      if extract_term(item) == match[0]:
        return item

class TelegramAPI:
  def __init__(self, key, chat_id) -> None:
    self.key = key
    self.chat_id = chat_id

  logger = logging.getLogger()

  def send_message(self, message):
    url = f'{BASE_TELEGRAM_API_URL}{self.key}/sendMessage?chat_id={self.chat_id}&text={_encode(message)}'

    LOGGER.debug(f'GET {url}')

    requests.get(url)
