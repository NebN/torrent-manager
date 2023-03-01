import unittest
from src import torrent
from src.model import Category, SeasonTorrent, EpisodeTorrent, MovieTorrent

class TorrentTest(unittest.TestCase):

  def test_from_torrent_info_movie_year(self):
    name = 'The Matrix (1999)'
    path = '/some/path'
    t = torrent.from_torrent_info(name, Category.MOVIE, path)
    expected = MovieTorrent(name=name, root_dir=path, category=Category.MOVIE, title='The Matrix', year=1999)
    self.assertEqual(expected, t)

  def test_from_torrent_info_movie(self):
    name = 'The Matrix '
    path = '/some/path'
    t = torrent.from_torrent_info(name, Category.MOVIE, path)
    expected = MovieTorrent(name=name, root_dir=path, category=Category.MOVIE, title='The Matrix', year=None)
    self.assertEqual(expected, t)

  def test_from_torrent_info_tv_episode(self):
    name = 'The Last of Us S01E04'
    path = '/some/path'
    t = torrent.from_torrent_info(name, Category.TV, path)
    expected = EpisodeTorrent(name=name, root_dir=path, category=Category.TV, show_title='The Last of Us', season=1, episode=4)
    self.assertEqual(expected, t)

  def test_from_torrent_info_tv_season(self):
    name = 'The Last of Us S01'
    path = '/some/path'
    t = torrent.from_torrent_info(name, Category.TV, path)
    expected = SeasonTorrent(name=name, root_dir=path, category=Category.TV, show_title='The Last of Us', seasons={1})
    self.assertEqual(expected, t)
  
  def test_from_torrent_info_tv_multiple_seasons(self):
    name = 'The Last of Us S01-3'
    path = '/some/path'
    t = torrent.from_torrent_info(name, Category.TV, path)
    expected = SeasonTorrent(name=name, root_dir=path, category=Category.TV, show_title='The Last of Us', seasons={1,2,3})
    self.assertEqual(expected, t)


if __name__ == '__main__':
  unittest.main()