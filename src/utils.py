from datetime import datetime
from itertools import groupby
from pathlib import Path
import functools
import titlecase as tcase
import math
import re
import os

NOW = datetime.now()

def walk_file_or_directory(path):
  p = Path(path)
  if p.is_file():
    yield p.parent, [], [p.name]
  else:
    for x in os.walk(path):
      yield x


def last_index_of(x, xs):
  ix = -1
  for index, item in enumerate(xs):
    if x == item:
      ix = index
  return ix
  

def unique_elements(items):
  return len(set(items))


def max_repeats(items):
  return max([len(list(group)) for _, group in groupby(sorted(items))])


def groupby_unsorted(items, key):
  return groupby(sorted(items, key=key), key=key)


def pop_first(items, predicate):
  for ix, item in enumerate(items):
    if predicate(item):
      return items.pop(ix)


def chunk_list(items, chunk_size):
  for i in range(0, len(items), chunk_size):
    yield items[i:i + chunk_size]


def replace_string_in_ranges(original, replacement, *ranges):
  if len(ranges) == 0:
    return original
  
  start, end = ranges[0]
  
  # can't replace with an empty string
  adjusted_replacement = replacement if len(replacement) > 0 else ' ' 

  len_range = len(range(start, end))
  len_replacement = len(adjusted_replacement)
  replacement_length_offset = len_replacement - len_range
  

  if replacement_length_offset > 0:
    adjusted_replacement = adjusted_replacement[:len_range]
  elif replacement_length_offset < 0:
    adjusted_replacement = (adjusted_replacement * math.ceil(len_range/len_replacement))[:len_range]

  replaced = original[:start] + adjusted_replacement + original[start+len_range:]
  
  return replace_string_in_ranges(replaced, replacement, *ranges[1:])


_SPACE_REGEX = re.compile('\s+')
def replace_spaces(original, replacement):
  return _SPACE_REGEX.sub(replacement, original)


def suffix(file):
  return Path(file).suffix


def zfill_2(string):
  return str(string).zfill(2)


_CHARS_TO_REMOVE = ["'", "-"]
def torrentcase(string):
  cleaned = functools.reduce(lambda s, c : s.replace(c, ''), _CHARS_TO_REMOVE, string)
  return replace_spaces(tcase.titlecase(cleaned), '.')
