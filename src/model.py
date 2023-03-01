from dataclasses import dataclass
from enum import Enum, auto


class TorrentManagerException(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class Category(Enum):
  MOVIE = auto()
  TV = auto()

  def from_string(string):
    lowercase = string.lower()
    if 'movie' in lowercase:
      return Category.MOVIE
    if 'tv' in lowercase:
      return Category.TV
    raise TorrentManagerException(f'Invalid category: {string}')


class Language(Enum):
  ENGLISH = 'en'
  ITALIAN = 'it'
  OTHER = None

  def __init__(self, label) -> None:
    super().__init__()
    self.label = label


@dataclass
class Torrent:
  name: str
  root_dir: str
  category: Category


@dataclass
class MovieTorrent(Torrent):
  title: str
  year: int


@dataclass
class EpisodeTorrent(Torrent):
  show_title: str
  season: int
  episode: int


@dataclass
class SeasonTorrent(Torrent):
  show_title: str
  seasons: set[int]


@dataclass
class SubtitleFile:
  path: str
  language: Language


@dataclass
class MovieFile:
  path: str
  title: str
  year: int = None
  subtitles: list[SubtitleFile] = None


@dataclass
class EpisodeFile:
  path: str
  show_title: str
  season: int
  episode: int
  subtitles: list[SubtitleFile] = None

