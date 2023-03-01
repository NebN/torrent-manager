import os
import shutil
import logging
from enum import Enum, auto
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import magic

from src import utils
from src.model import *
from src.regex import EpisodeDigitRegex, EpisodeRegex, MassEpisodeRegex

logger = logging.getLogger()

class FileType(Enum):
  VIDEO = auto()
  IMAGE = auto()
  SUBTITLE = auto()
  TEXT = auto()
  OTHER = auto()

  @staticmethod
  def from_path(path):
    file_type = magic.Magic(mime=True).from_file(path)
    if 'subrip' in file_type:
      return FileType.SUBTITLE
    if 'video' in file_type:
      return FileType.VIDEO
    if 'text' in file_type:
      return FileType.TEXT
    if 'image' in file_type:
      return FileType.IMAGE
    
    return FileType.OTHER



def identify_relevant_files(torrent):
  match torrent:
    case MovieTorrent():
      return _identify_movie_files(torrent)
    case EpisodeTorrent():
      return _identify_episode_files(torrent)
    case SeasonTorrent():
      return _identify_season_files(torrent)


def _identify_subtitle_language(fullpath):
  filename = Path(fullpath).stem
  for language in Language:
    if language.label in filename:
      return language
  return Language.OTHER


def copy_files(files, destination_root, group):
  files_with_destinations = [(_destination_folder(destination_root, f), f) for f in files]
  all_destinations = set([d for d, _ in files_with_destinations])
  for destination in all_destinations:
    logger.info('mkdir %s', destination)
    Path(destination).mkdir(mode=0o775, parents=True, exist_ok=True)
    if group:
      shutil.chown(destination, group=group)

  with ThreadPoolExecutor(max_workers=os.cpu_count()) as e:
    for destination, file in files_with_destinations:
      filename = _filename(file)
      full_destination = os.path.join(destination, filename)
      logger.info('copy %s -> %s', file.path, full_destination)
      e.submit(shutil.copy,file.path, full_destination)


def _destination_folder(destination_root, file):
  def folder():
    match file:
      case MovieFile() as f:
        full_title = f.title + f'.{f.year}' if f.year is not None else ''
        return full_title
      case EpisodeFile() as f:
        return os.path.join(f.show_title, utils.zfill_2(f.season))

  return os.path.join(destination_root, utils.torrentcase(folder()))


def _filename(file):
  def filename():
    match file:
      case MovieFile() as f:
        return f.title + (f' {f.year}' if f.year is not None else '')
      case EpisodeFile() as f:
        return f'{f.show_title} S{utils.zfill_2(f.season)}E{utils.zfill_2(f.episode)}'
  return utils.torrentcase(filename()) + utils.suffix(file.path)


def _vides_and_subtitles(torrent):
  subtitle_files = []
  video_files = []

  for root, dirs, files in utils.walk_file_or_directory(torrent.root_dir):
    for file in files:
      file_path = os.path.join(root, file)
      match FileType.from_path(os.path.join(root, file)):
        case FileType.VIDEO:
          video_files.append(file_path)
        case FileType.SUBTITLE:
          subtitle_files.append(file_path)

  if not video_files:
    raise TorrentManagerException(f'{torrent.root_dir} has no video files')

  subtitles = [SubtitleFile(s, _identify_subtitle_language(s)) for s in subtitle_files]
  relevant_subtitles = [s for s in subtitles if s.language != Language.OTHER]

  return video_files, relevant_subtitles


def _identify_single_video_files(torrent):
  videos, subtitles = _vides_and_subtitles(torrent)
  relevant_video_file = max(videos, key=lambda v: os.path.getsize(v))
  return relevant_video_file, subtitles


def _identify_movie_files(torrent):
  video, subtitles = _identify_single_video_files(torrent)
  movie_file = MovieFile(path=video, \
    title=torrent.title, \
    year=torrent.year, \
    subtitles=subtitles)
  return [movie_file]


def _identify_episode_files(torrent):
  video, subtitles = _identify_single_video_files(torrent)

  episode_file = EpisodeFile(path=video, \
    show_title=torrent.show_title, \
    season=torrent.season, \
    episode=torrent.episode, \
    subtitles=subtitles)

  return [episode_file]


def _identify_season_files(torrent):
  videos, subtitles = _vides_and_subtitles(torrent)
  extract_function = _extract_episodes_from_single_season if len(torrent.seasons) == 1 else _extract_season_and_episode_from_multiple_seasons
  return [EpisodeFile(path=file, show_title=torrent.show_title, season=s, episode=e) for (s, e), file in extract_function(videos, torrent)]


def _extract_episodes_from_single_season(filenames, torrent):
  len_filenames = len(filenames)
  season = next(iter(torrent.seasons))

  def inner(regex):
    searched = [regex(f) for f in filenames]
    if all([r.successful_match() for r in searched]):
      episodes_and_seasons_numbers = [(season, m.episode()) for m in searched]
      if len(set(episodes_and_seasons_numbers)) == len_filenames:
        # We have a different match for each filename
        return list(zip([(int(e), int(s)) for e, s in episodes_and_seasons_numbers], filenames))

  for regex in [EpisodeRegex, EpisodeDigitRegex]:
    res = inner(regex)
    if res is not None:
      return res


def _extract_season_and_episode_from_multiple_seasons(filenames, torrent):
    return MassEpisodeRegex(filenames, torrent).extract_season_and_episodes()
    
