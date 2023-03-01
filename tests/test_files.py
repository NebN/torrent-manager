import os 
import unittest
from src import files as f
from src.model import *

class FilesTest(unittest.TestCase):

  TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), *['test_data'])

  def test_extract_episodes_from_single_season(self):
    files = [
      'Severance.S01E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      'Severance.S01E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      'Severance.S01E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      'Severance.S01E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir', category=Category.TV, show_title='Severance', seasons={1})
    expected = [((1, ix+1), file) for ix, file in enumerate(files[::-1])][::-1]
    res = f._extract_episodes_from_single_season(files, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_from_single_season_bad_format(self):
    files = [
      'Severance.9.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.8.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      'Severance.7.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      'Severance.6.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.5.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.4.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      'Severance.3.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.2.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.1.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir', category=Category.TV, show_title='Severance', seasons={1})
    expected = [((1, ix+1), file) for ix, file in enumerate(files[::-1])][::-1]
    res = f._extract_episodes_from_single_season(files, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_from_single_season_miniseries(self):
    files = [
      'TheShowName.Chapter.9.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.8.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.7.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      'TheShowName.Chapter.6.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.5.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.4.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      'TheShowName.Chapter.3.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.2.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'TheShowName.Chapter.1.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='TheShowName S01', root_dir='/somedir', category=Category.TV, show_title='TheShowName', seasons={1})
    expected = [((1, ix+1), file) for ix, file in enumerate(files[::-1])][::-1]
    res = f._extract_episodes_from_single_season(files, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_multiple_seasons(self):
    season_1 = [
      'Severance.S01E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      'Severance.S01E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S01E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      'Severance.S01E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      'Severance.S01E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    season_2 = [
      'Severance.S02E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S02E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S02E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S02E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      'Severance.S02E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S02E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      'Severance.S02E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      'Severance.S02E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      'Severance.S02E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir', category=Category.TV, show_title='Severance', seasons={1,2})
    expected = [((1, ix+1), file) for ix, file in enumerate(season_1)] + [((2, ix+1), file) for ix, file in enumerate(season_2)]
    res = f._extract_season_and_episode_from_multiple_seasons(season_1 + season_2, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_multiple_seasons_not_in_video_title(self):
    season_1 = [
      '/somedir/season.01/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/season.01/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/season.01/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/season.01/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    season_2 = [
      '/somedir/season.02/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/season.02/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/season.02/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/season.02/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir', category=Category.TV, show_title='Severance', seasons={1,2})
    expected = [((1, ix+1), file) for ix, file in enumerate(season_1)] + [((2, ix+1), file) for ix, file in enumerate(season_2)]
    res = f._extract_season_and_episode_from_multiple_seasons(season_1 + season_2, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_multiple_seasons_not_in_video_title_two_folders_up(self):
    season_1 = [
      '/somedir/season.01/Episode01/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode02/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode03/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode04/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/season.01/Episode05/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode06/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode07/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/season.01/Episode08/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/season.01/Episode09/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    season_2 = [
      '/somedir/season.02/Episode01/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode02/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode03/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode04/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/season.02/Episode05/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode06/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode07/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/season.02/Episode08/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/season.02/Episode09/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir', category=Category.TV, show_title='Severance', seasons={1,2})
    expected = [((1, ix+1), file) for ix, file in enumerate(season_1)] + [((2, ix+1), file) for ix, file in enumerate(season_2)]
    res = f._extract_season_and_episode_from_multiple_seasons(season_1 + season_2, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_multiple_seasons_not_in_video_title_two_folders_up_and_misleading_root_folder(self):
    season_1 = [
      '/somedir/fake.season.02/season.01/Episode01/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode02/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode03/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode04/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode05/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode06/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode07/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode08/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/Episode09/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    season_2 = [
      '/somedir/fake.season.02/season.02/Episode01/Severance.E01.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode02/Severance.E02.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode03/Severance.E03.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode04/Severance.E04.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode05/Severance.E05.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode06/Severance.E06.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode07/Severance.E07.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode08/Severance.E08.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode09/Severance.E09.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir/fake.season.02', category=Category.TV, show_title='Severance', seasons={1,2})
    expected = [((1, ix+1), file) for ix, file in enumerate(season_1)] + [((2, ix+1), file) for ix, file in enumerate(season_2)]
    res = f._extract_season_and_episode_from_multiple_seasons(season_1 + season_2, torrent)
    self.assertEqual(expected, res)


  def test_extract_episodes_multiple_seasons_not_in_video_title_only_two_folders_up_and_misleading_root_folder(self):
    season_1 = [
      '/somedir/fake.season.02/season.01/01/Severance.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/02/Severance.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/03/Severance.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/04/Severance.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/05/Severance.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/06/Severance.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/07/Severance.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/fake.season.02/season.01/08/Severance.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.01/09/Severance.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    season_2 = [
      '/somedir/fake.season.02/season.02/Episode01/Severance.Good.News.About.Hell.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode02/Severance.Half.Loop.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode03/Severance.In.Perpetuity.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode04/Severance.The.You.You.Are.1080p.ATVP.WEB-DL.DDP5.1.H264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode05/Severance.The.Grim.Barbarity.of.Optics.and.Design.1080.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode06/Severance.Hide.and.Seek.1080p.ATVP.WEB-DL.DDP5.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode07/Severance.Defiant.Jazz.1080p.ATVP.WEB-DL.DDP5.1.H.264EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode08/Severance.Whats.for.Dinner.1080p.ATVP.1.H.264-EniaHD.avi',
      '/somedir/fake.season.02/season.02/Episode09/Severance.The.We.We.Are.1080p.ATVp.WEB-DL.DDP5.1.H.264-EniaHD.avi'
    ]

    torrent = SeasonTorrent(name='Severance S01', root_dir='/somedir/fake.season.02', category=Category.TV, show_title='Severance', seasons={1,2})
    expected = [((1, ix+1), file) for ix, file in enumerate(season_1)] + [((2, ix+1), file) for ix, file in enumerate(season_2)]
    res = f._extract_season_and_episode_from_multiple_seasons(season_1 + season_2, torrent)
    self.assertEqual(expected, res)

  def test_identify_relevant_files_movie(self):
    data_dir = os.path.join(FilesTest.TEST_DATA_PATH, 'the.matrix')
    movie_path = os.path.join(data_dir, 'the.matrix.1999.avi')
    subtitles = SubtitleFile(path=os.path.join(data_dir, 'english.srt'), language=Language.ENGLISH)
    t = MovieTorrent(name='The Matrix (1999)', root_dir=data_dir, category=Category.MOVIE, title='The Matrix', year=1999)
    expected = [MovieFile(path=movie_path, title='The Matrix', year=1999, subtitles=[subtitles])]
    
    res = f.identify_relevant_files(t)

    self.assertEqual(expected, res)


  def test_identify_relevant_files_episode(self):
    data_dir = os.path.join(FilesTest.TEST_DATA_PATH, 'the.last.of.us.s01e03')
    episode_path = os.path.join(data_dir, 'the.last.of.us.s01e03.avi')
    subtitles = SubtitleFile(path=os.path.join(data_dir, 'ita.srt'), language=Language.ITALIAN)
    t = EpisodeTorrent(name='The Last of Us S01E03', root_dir=data_dir, category=Category.TV, show_title='The Last of Us', season=1, episode=3)
    expected = [EpisodeFile(path=episode_path, show_title='The Last of Us', season=1, episode=3, subtitles=[subtitles])]
    
    res = f.identify_relevant_files(t)

    self.assertEqual(expected, res)


  def test_identify_relevant_files_episode(self):
    data_dir = os.path.join(FilesTest.TEST_DATA_PATH, 'the.last.of.us.s01')
    episodes = [EpisodeFile(os.path.join(data_dir, p), 'The Last of Us', season=1, episode=e) for e, p in [(e, f'the.last.of.us.s01e0{e}.avi') for e in [1,2,3]]]
    t = SeasonTorrent(name='The Last of Us S01', root_dir=data_dir, category=Category.TV, show_title='The Last of Us', seasons={1})
    expected = episodes
    
    res = f.identify_relevant_files(t)

    # misleading name, but actually checks for equality on each item, not just the amount
    self.assertCountEqual(expected, res)


  def test_identify_relevant_files_seasons(self):
    data_dir = os.path.join(FilesTest.TEST_DATA_PATH, 'the.last.of.us')
    season_1 = [EpisodeFile(os.path.join(data_dir, p), 'The Last of Us', season=1, episode=e) for e, p in [(e, f'the.last.of.us.s01e0{e}.avi') for e in [1,2,3]]]
    season_2 = [EpisodeFile(os.path.join(data_dir, p), 'The Last of Us', season=2, episode=e) for e, p in [(e, f'the.last.of.us.s02e0{e}.avi') for e in [1,2]]]
    episodes = season_1 + season_2
    t = SeasonTorrent(name='The Last of Us S01', root_dir=data_dir, category=Category.TV, show_title='The Last of Us', seasons={1,2})
    expected = episodes
    
    res = f.identify_relevant_files(t)

    # misleading name, but actually checks for equality on each item, not just the amount
    self.assertCountEqual(expected, res)


  def test_identify_relevant_files_seasons_bad_names(self):
    data_dir = os.path.join(FilesTest.TEST_DATA_PATH, 'the.last.of.us.badnames')
    season_1 = [EpisodeFile(os.path.join(data_dir, '1', p), 'The Last of Us', season=1, episode=e) for e, p in [(e, f'the.last.of.us.1.{e}.avi') for e in [1,2,3]]]
    season_2 = [EpisodeFile(os.path.join(data_dir, '2', p), 'The Last of Us', season=2, episode=e) for e, p in [(e, f'the.last.of.us.1.{e}.avi') for e in [1,2]]]
    episodes = season_1 + season_2
    t = SeasonTorrent(name='The Last of Us S01', root_dir=data_dir, category=Category.TV, show_title='The Last of Us', seasons={1,2})
    expected = episodes
    
    res = f.identify_relevant_files(t)

    # misleading name, but actually checks for equality on each item, not just the amount
    self.assertCountEqual(expected, res)

if __name__ == '__main__':
  unittest.main()