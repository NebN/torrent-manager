import unittest
from src import utils


class TestUtils(unittest.TestCase):

  def test_replace_string_in_ranges(self):
    res = utils.replace_string_in_ranges('ABCDEFG', '_', (4,5))
    expected = 'ABCD_FG'
    self.assertEqual(res, expected)

    res = utils.replace_string_in_ranges('ABCDEFG', '_', (4,6))
    expected = 'ABCD__G'
    self.assertEqual(res, expected)

    res = utils.replace_string_in_ranges('ABCDEFG', '_', (4,7))
    expected = 'ABCD___'
    self.assertEqual(res, expected)

    res = utils.replace_string_in_ranges('ABCDEFG', '_', (4,5), (1,3))
    expected = 'A__D_FG'
    self.assertEqual(res, expected)

    res = utils.replace_string_in_ranges('ABCDEFG', '1234', (4,5), (1,3))
    expected = 'A12D1FG'
    self.assertEqual(res, expected)
    
    res = utils.replace_string_in_ranges('ABCDEFG', '1234', (0,6))
    expected = '123412G'
    self.assertEqual(res, expected)
        
    res = utils.replace_string_in_ranges('ABCDEFG', '123', (0,1), (3,7))
    expected = '1BC1231'
    self.assertEqual(res, expected)
    
    res = utils.replace_string_in_ranges('ABCDEFG', '', (0,1), (3,7))
    expected = ' BC    '
    self.assertEqual(res, expected)


  def test_pop_first(self):
    list = [1,2,3,4]
    res = utils.pop_first(list, lambda n: n == 2)
    self.assertEquals(2, res)
    self.assertEquals([1,3,4], list)

    list = ['A', 'B', 'c', 'D']
    res = utils.pop_first(list, lambda s: s.islower())
    self.assertEquals('c', res)
    self.assertEquals(['A', 'B', 'D'], list)
    

    list = ['A', 'B', 'c', 'D', 'e']
    res = utils.pop_first(list, lambda s: s.islower())
    self.assertEquals('c', res)
    self.assertEquals(['A', 'B', 'D', 'e'], list)


  def test_replace_spaces(self):
    res = utils.replace_spaces('This text has spaces', '.')
    expected = 'This.text.has.spaces'
    self.assertEqual(expected, res)

    res = utils.replace_spaces('This  text has  more    spaces', '.')
    expected = 'This.text.has.more.spaces'
    self.assertEqual(expected, res)