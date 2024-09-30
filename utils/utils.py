"""
Name: test_registration.py
Author: Ryan Gascoigne-Jones

Purpose: Utility functions
"""

def check_contains_upper_and_num(string: str) -> bool:
  """Checks if the string contains any uppercase characters"""

  upper_found: bool = False
  number_found: bool = False

  for char in string:
    if char.isupper():
      upper_found = True
    elif char.isnumeric():
      number_found = True
      
    if upper_found and number_found:
      return True
    
  return False