"""
Name: test_check_user_input.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the checking functions in check_user_input.py.
"""

import unittest
from datetime import date
from flask import Response
import json
# Local imports
from utils import check_username, check_password, check_email, check_dob, \
  check_number, check_input_present

class CheckInputsTest(unittest.TestCase):
  """Tests the check functions in check_user_input.py"""

  def setUp(self):
    """Set up mock data"""

    # Valid input (to be changed by test)
    self.valid_data: dict = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567891234567"
    }

    self.expected: list = ["username", "password", "email", "dob"]

  
  ## check_input_present() Tests ##

  def test_check_input_present_valid_all_present(self):
    """Tests checking all input arguments are present with a full valid
    set"""

    # Passes valid data and expected arguments
    response: Response = check_input_present(user_input=self.valid_data,
      expected=self.expected)
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_input_present_valid_ccn_absent(self):
    """Tests checking all input arguments are present with a valid set
    with only ccn missing which is an optional argument"""

    # Removes ccn from input which is not expected
    valid_data_copy: dict = self.valid_data.copy()
    valid_data_copy.pop('credit_card_number')

    # Passes valid data and expected arguments
    response: Response = check_input_present(user_input=valid_data_copy,
      expected=self.expected)
    
    self.assertEqual(response.status_code, 200)

  def test_check_input_present_invalid_absent(self):
    """Tests checking all input arguments are present with a valid set
    with only ccn missing which is an optional argument"""

    # Removes email from input which is expected
    invalid_data: dict = self.valid_data.copy()
    invalid_data.pop('email')

    # Passes invalid data and expected arguments
    response: Response = check_input_present(user_input=invalid_data,
      expected=self.expected)
    
    # Checks the response is 400 Bad Request and the error message is
    # correct.
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "email must be provided.")
    

  ## check_username() Tests ##

  def test_check_username_valid(self):
    """Tests checking of valid username"""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username=self.valid_data['username'],
                                        existing_users=[])
    
    self.assertEqual(response.status_code, 200)

  def test_check_username_valid_existing_users_populated(self):
    """Tests checking of valid username"""

    valid_data_copy: dict = self.valid_data.copy()
    valid_data_copy['username'] = "user456"

    # Passes valid data and empty list of existing users
    response: Response = check_username(username=self.valid_data['username'],
                                        existing_users=[valid_data_copy])
    
    self.assertEqual(response.status_code, 200)

  def test_check_username_invalid_non_alphanumeric(self):
    """Tests checking an invalid username with non alphanumeric
    characters in it."""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username='user123?',
                                        existing_users=[])
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Username must contain only letters and numbers.")

  def test_check_username_invalid_space(self):
    """Tests checking an invalid username with a space in it."""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username='user 123',
                                        existing_users=[])
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Username cannot contain spaces.")

  def test_check_username_invalid_taken(self):
    """Tests checking an invalid username that is already taken by
    another user"""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username=self.valid_data['username'],
                                        existing_users=[self.valid_data])
    
    self.assertEqual(response.status_code, 409)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Username already taken.")
    
    
  ## check_password() Tests ##

  def test_check_password_valid(self):
    """Tests checking a valid password"""

    # Passes valid data and expected arguments
    response: Response = check_password(password=self.valid_data['password'])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_password_invalid_length(self):
    """Tests checking an invalid password that is too short"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "Pass123"

    # Checks the response's status code is as expected
    response: Response = check_password(password=invalid_data['password'])
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Password must contain a minimum of 8 characters.")

  def test_check_password_invalid_upper(self):
    """Tests checking an invalid password that doesn't contain an upper
    case character."""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "pass1234"

    # Checks the response's status code is as expected
    response: Response = check_password(password=invalid_data['password'])
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Password must contain at least one of both uppercase " \
                     "characters and numbers.")

  def test_check_password_invalid_number(self):
    """Tests checking an invalid password that doesn't contain a
    number."""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "Password"

    # Checks the response's status code is as expected
    response: Response = check_password(password=invalid_data['password'])
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Password must contain at least one of both uppercase " \
                     "characters and numbers.")


if __name__ == "__main__":
  unittest.main()