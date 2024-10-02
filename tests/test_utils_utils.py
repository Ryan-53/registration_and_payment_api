"""
Name: test_check_user_input.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the utility functions in utils.py.
"""

import unittest
# Local imports
from utils import check_contains_upper_and_num

class UtilsTest(unittest.TestCase):
  """Tests utility functions in utils.py"""

  ## check_contains_upper_and_num() Tests ##

  def test_check_contains_upper_and_num_valid(self):
    """Tests checking a valid string"""

    self.assertTrue(check_contains_upper_and_num(string="Upper123"))

  def test_check_contains_upper_and_num_invalid_no_upper(self):
    """Tests checking an invalid string containing no upper case characters"""

    self.assertFalse(check_contains_upper_and_num(string="lower123"))

  def test_check_contains_upper_and_num_invalid_no_number(self):
    """Tests checking an invalid string containing no numbers"""

    self.assertFalse(check_contains_upper_and_num(string="UpperNoNum"))

  def test_check_contains_upper_and_num_invalid_no_number_or_upper(self):
    """Tests checking an invalid string containing no numbers"""

    self.assertFalse(check_contains_upper_and_num(string="lowernonum"))