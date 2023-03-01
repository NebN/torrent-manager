import re
from src.model import Category, MovieTorrent, EpisodeTorrent, SeasonTorrent
from src.regex import TVEpisodeRegex, TVSeasonRegex


MOVIE_REGEX = re.compile(r'(.+)\((19\d\d|20\d\d)\)')

def from_torrent_info(name, category, path):
  match category:
    case Category.MOVIE:
      if name_match := MOVIE_REGEX.match(name):
        title = name_match.group(1)
        year = int(name_match.group(2))
      else:
        title = name
        year = None
      return MovieTorrent(name=name, root_dir=path, category=category, title=title.strip(), year=year)

    case Category.TV:
      episode_match = TVEpisodeRegex(name)
      if episode_match.successful_match():
        show_title = episode_match.title()
        season = episode_match.season()
        episode = episode_match.episode()
        return EpisodeTorrent(name=name, root_dir=path, category=category, show_title=show_title, season=season, episode=episode)
      else:
        name_match = TVSeasonRegex(name)
        show_title = name_match.title()
        season_from = name_match.season_from()
        season_to = name_match.season_to()
        seasons = set(range(season_from, season_to+1))
        return SeasonTorrent(name=name, root_dir=path, category=category, show_title=show_title, seasons=seasons)
