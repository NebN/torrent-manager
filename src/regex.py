import re
from re import Match, Pattern
import time
import itertools
from dataclasses import dataclass
from pathlib import Path
from abc import ABC
from src import utils


MOVIE_REGEX = re.compile(r'(.+)\((19\d\d|20\d\d)\)')


class TorrentRegex(ABC):
  def __init__(self, matched) -> None:
    super().__init__()
    self.matched = matched

  def successful_match(self) -> bool:
    self.matched is not None


class TVEpisodeRegex(TorrentRegex):
  REGEX = re.compile(r'(.+?)\s+(?:[Ss](\d{1,2})[Ee](\d{1,2}))')

  def __init__(self, string) -> None:
    super().__init__(TVEpisodeRegex.REGEX.match(string))

  def successful_match(self) -> bool:
    return self.matched is not None

  def title(self):
    return self.matched.group(1).strip()

  def season(self):
    return int(self.matched.group(2))

  def episode(self):
    return int(self.matched.group(3))



class TVSeasonRegex(TorrentRegex):
  REGEX = re.compile(r'(.+?)\s+(?:[Ss](\d{1,2})(?:-(\d{1,2}))?)')

  def __init__(self, string) -> None:
    super().__init__(TVSeasonRegex.REGEX.match(string))

  def successful_match(self) -> bool:
    return self.matched is not None

  def title(self):
    return self.matched.group(1).strip()

  def season_from(self):
    return int(self.matched.group(2))

  def season_to(self):
    return int(self.matched.group(3)) if self.matched.group(3) is not None else self.season_from()



class EpisodeRegex(TorrentRegex):
  REGEX = re.compile(r'(?:[Ss](\d{1,2})?)?.?[Ee](?:[Pp](?:[Ss]|(?:[Ii][Ss][Oo][Dd]))?)?(\d{1,2})')

  def __init__(self, string) -> None:
    super().__init__(EpisodeRegex.REGEX.search(string))

  def successful_match(self) -> bool:
    return self.matched is not None

  def season(self):
    return int(self.matched.group(1)) if self.matched.group(1) is not None else None

  def episode(self):
    return int(self.matched.group(2))


class EpisodeDigitRegex(TorrentRegex):
  REGEX = re.compile(r'(\d+)')

  def __init__(self, string) -> None:
    super().__init__(EpisodeDigitRegex.REGEX.search(string))

  def successful_match(self) -> bool:
    return self.matched is not None

  def episode(self):
    return int(self.matched.group(1))



class MassEpisodeRegex():

  @dataclass
  class RegexConfidence:
    regex: Pattern
    confidence: int

  EPISODE_REGEX = re.compile(r'(?:[Ss](\d{1,2})).?[Ee](?:[Pp](?:[Ss]|(?:[Ii][Ss][Oo][Dd]))?)?(\d{1,2})')
  WORD_REGEX = re.compile(r'([a-zA-Z0-9]+)')

  ONLY_EPISODE_REGEX = RegexConfidence(re.compile(r'[Ee](?:[Pp](?:[Ss]|(?:[Ii][Ss][Oo][Dd]))?)?(\d{1,2})'), 2)
  ONLY_SEASON_REGEX = RegexConfidence(re.compile(r'[Ss](?:[Ee][Aa][Ss][Oo][Nn])?(\d{1,2})'), 2)
  DIGITS_REGEX = RegexConfidence(re.compile(r'(?<!\d)(\d{1,2})(?!\d)'), 1)

  def __init__(self, episodes, torrent) -> None:
    episodes_info = [self.EpisodeInfo(e, torrent) for e in episodes]
    len_episodes = len(episodes)
    matches_to_replace = []

    for ix_of_slice, parts in enumerate(zip(*[e.searchable_parts for e in episodes_info])):
      matches_for_parts = [list(MassEpisodeRegex.WORD_REGEX.finditer(part)) for part in parts]
      for ix_of_part_in_slice, matches in enumerate(matches_for_parts):
        other_parts = matches_for_parts[:ix_of_part_in_slice] + matches_for_parts[ix_of_part_in_slice+1:]
        for match in matches:
          matching_matches = [(ix_of_slice, match)]
          for other_matches in other_parts:
            popped = utils.pop_first(other_matches, lambda m: m.groups() == match.groups())
            if popped is not None:
              matching_matches.append((ix_of_slice, popped))
          if len(matching_matches) == len_episodes:
            matches_to_replace.extend(matching_matches)

    for chunk in utils.chunk_list(matches_to_replace, len_episodes):
      for ep, replacement in zip(episodes_info, chunk):
        ix_part_to_replace, match = replacement
        replaced = utils.replace_string_in_ranges(ep.searchable_parts[ix_part_to_replace], ' ', match.span())
        ep.searchable_parts[ix_part_to_replace] = replaced

    self.episodes = episodes_info
    self.torrent = torrent


  class EpisodeInfo():
    def __init__(self, fullpath, torrent) -> None:
      self.fullpath = fullpath
      path = Path(fullpath.replace(torrent.root_dir, '', 1))
      # name first, then folders in reverse order
      # removing everything up to and including the torrent's root directory
      # example: /home/user/torrents/tv/show_name/seasons/season01/episode01.mp4
      # torrent root directory: /home/user/torrents/tv/show_name
      # becomes: ['episode01.mp4', 'season01', 'seasons']
      self.searchable_parts = list(path.parts[-1::-1])

  class EpisodeGuess():
    def __init__(self, episode_info, torrent) -> None:
      self.episode_info = episode_info
      self.torrent = torrent
      self.plausible_seasons = set()
      self.plausible_seasons_matches = []
      self.plausible_episodes = set()
      self.plausible_episodes_matches = []
      self.season_guess = None
      self.episode_guess = None
      self.season = None
      self.episode = None
    
    def __repr__(self):
      return f'{self.episode_info.fullpath}'

    @dataclass
    class MatchConfidence():
      match: Match
      confidence: int
    
    def match_confidence(self, match, confidence):
      return MassEpisodeRegex.EpisodeGuess.MatchConfidence(match, confidence)

    def accumulating_plausible_seasons_and_episodes(self, season_regex_confidence, episode_regex_confidence):
      len_parts = len(self.episode_info.searchable_parts)
      season_regex = season_regex_confidence.regex
      episode_regex = episode_regex_confidence.regex
      season_confidence = season_regex_confidence.confidence
      episode_confidence = episode_regex_confidence.confidence

      for part_ix, (seasons, episodes) in enumerate([(list(season_regex.finditer(p)), list(episode_regex.finditer(p))) for p in self.episode_info.searchable_parts]):
        self.plausible_seasons.update({int(match.group(1)) for match in seasons if int(match.group(1)) in self.torrent.seasons})
        self.plausible_episodes.update({int(match.group(1)) for match in episodes})
        self.plausible_seasons_matches.extend([self.match_confidence(match, part_ix * episode_confidence) for match in seasons if int(match.group(1)) in self.torrent.seasons])
        self.plausible_episodes_matches.extend([self.match_confidence(match, (len_parts - part_ix)  * season_confidence) for match in episodes])
        yield self


    def combinations(self):
      def generator():
        for s in self.plausible_seasons_matches:
          for e in self.plausible_episodes_matches:
            if s.match.span() != e.match.span():
              yield (s.confidence + e.confidence), int(s.match.group(1)), int(e.match.group(1))
      return [(s, e) for _, s, e in sorted(generator(), key=lambda c_s_e: -c_s_e[0])]


  def extract_season_and_episodes(self):
    attempts = [
      self._attempt_simultaneous_extraction,
      self._attempt_separate_extraction
    ]

    for attempt in attempts:
      if res := attempt():
        return res

  def _attempt_separate_extraction(self):
    guesses = [MassEpisodeRegex.EpisodeGuess(e, self.torrent) for e in self.episodes]
    regex_combinations = [
      (MassEpisodeRegex.ONLY_SEASON_REGEX, MassEpisodeRegex.ONLY_EPISODE_REGEX),
      (MassEpisodeRegex.DIGITS_REGEX, MassEpisodeRegex.ONLY_EPISODE_REGEX),
      (MassEpisodeRegex.DIGITS_REGEX, MassEpisodeRegex.DIGITS_REGEX)
    ]

    for s_regex, e_regex in regex_combinations:
      for accumulating_guess in zip(*[g.accumulating_plausible_seasons_and_episodes(s_regex, e_regex) for g in guesses]):
        all_seasons = set().union(*[guess.plausible_seasons for guess in accumulating_guess])
        all_episodes = set().union(*[guess.plausible_episodes for guess in accumulating_guess])
        len_episodes = len(self.episodes)
        season_minimum_length = len_episodes / len(self.torrent.seasons)
        combination_guess_list = [(combination, g) for g in accumulating_guess for combination in g.combinations()]
        guesses_grouped_by_combinations = [(key, [v for _, v in iterator]) for key, iterator in utils.groupby_unsorted(combination_guess_list, key=lambda c_g: c_g[0])]
        len_guesses_grouped_by_combinations = len(guesses_grouped_by_combinations)

        if all_seasons == self.torrent.seasons and \
          len(all_episodes) >= season_minimum_length and \
            len_guesses_grouped_by_combinations == len_episodes:
          # we might have all the data we need
          
          indexes_of_correct_choice = [(-1, None)] * len_guesses_grouped_by_combinations
          
          # Python recursion sux :(
          ix_of_choice_to_change = 0

          while ix_of_choice_to_change < len_guesses_grouped_by_combinations and ix_of_choice_to_change > -1:

            combination, guesses = guesses_grouped_by_combinations[ix_of_choice_to_change]
            current_guess_ix, current_guess_name = indexes_of_correct_choice[ix_of_choice_to_change]
            available_guesses_for_this_ix = guesses[current_guess_ix+1:]


            already_taken_guesses = [guess for _, guess in indexes_of_correct_choice]
            next_guess = next(filter(lambda name: name not in already_taken_guesses, available_guesses_for_this_ix), None)
            if next_guess is None:
              indexes_of_correct_choice[ix_of_choice_to_change] = (-1, None)
              ix_of_choice_to_change -= 1
              continue

            next_guess_ix = guesses.index(next_guess)
            indexes_of_correct_choice[ix_of_choice_to_change] = (next_guess_ix, next_guess)

            ix_of_choice_to_change += 1
            continue
          
          if ix_of_choice_to_change > -1:
            return [(combination, available_guesses[ix].episode_info.fullpath) \
              for (combination, available_guesses), ix \
                in zip(guesses_grouped_by_combinations, [i for i, _ in indexes_of_correct_choice])]
        

  def _attempt_simultaneous_extraction(self):
    for searchable_elements in zip(*[e.searchable_parts for e in self.episodes]):
      for matches in zip(*[list(MassEpisodeRegex.EPISODE_REGEX.finditer(e)) for e in searchable_elements]):
        if None not in matches:
          seasons_and_episodes = [(int(m.group(1)), int(m.group(2))) for m in matches]
          if self._seasons_and_episodes_are_plausible(seasons_and_episodes):
            return list(zip(seasons_and_episodes, [e.fullpath for e in self.episodes]))
          elif not self._can_check_next_matches(matches):
            break


  def _can_check_next_matches(self, current_matches):
    return utils.unique_elements([m.span() for m in current_matches]) == 1 or \
      utils.unique_elements([m.groups() for m in current_matches]) == 1


  def _seasons_and_episodes_are_plausible(self, seasons_and_episodes):
    return set([s for s, e in seasons_and_episodes]) == set(self.torrent.seasons) and \
      utils.unique_elements(seasons_and_episodes) == len(seasons_and_episodes)

