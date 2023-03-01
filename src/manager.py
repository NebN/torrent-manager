from src.model import TorrentManagerException, Category
from src import files, torrent
import logging

class TorrentManager():
   
   logger = logging.getLogger()

   def __init__(self, conf) -> None:
     self.conf = conf
     

   def manage(self, category, name, fullpath):
      t = torrent.from_torrent_info(name, category, fullpath)
      TorrentManager.logger.info('Processing torrent: %s', t)
      
      relevant_files = files.identify_relevant_files(t)
      for f in relevant_files:
         TorrentManager.logger.info('File: %s', f)

      destination_root = self.conf['FOLDERS']['movies' if category == Category.MOVIE else 'tv']
      media_group = self.conf['USERS']['group']
      files.copy_files(relevant_files, destination_root, media_group)
