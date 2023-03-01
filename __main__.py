import os
import sys
import traceback
from src.manager import TorrentManager
from src.model import TorrentManagerException
import configparser
import logging
from logging import config
from src.model import Category
from src.api import TelegramAPI

ROOT_DIR = sys.path[0]
LOGGING_CONF_PATH = os.path.join(ROOT_DIR, 'logging.conf')
CONTEXT_CONF_PATH = os.path.join(ROOT_DIR, 'conf.ini')


logger = logging.getLogger()
telegram = None

try:

  if len(sys.argv) < 3:
    raise TorrentManagerException(f'3 arguments required(category, name, path). Arguments provided: {",".join(sys.argv)}')
    
  category = sys.argv[1]
  name = sys.argv[2]
  path = sys.argv[3] 
  
  if not os.path.exists(LOGGING_CONF_PATH):
    logger.warning(f'Logging configuration file not found, will continue with default logging behaviour. File should be {LOGGING_CONF_PATH}')
  else:
    logging.config.fileConfig(LOGGING_CONF_PATH)

  if not os.path.exists(CONTEXT_CONF_PATH):
    raise TorrentManagerException(f'Configuration file not found, please create it as {CONTEXT_CONF_PATH}')

  conf = configparser.ConfigParser()
  conf.read(CONTEXT_CONF_PATH)

  telegram = TelegramAPI(conf['TELEGRAM']['key'], conf['TELEGRAM']['chat_id'])

  category_enum = Category.from_string(category)

  manager = TorrentManager(conf)
  manager.manage(
    category=category_enum,
    name=name,
    fullpath=path
  )

except TorrentManagerException as e:
  logger.error(e)
  if telegram:
    telegram.send_message(str(e))
except Exception as e:
  trace = traceback.format_exc()
  logger.error(trace)
  if telegram:
    telegram.send_message(trace)
