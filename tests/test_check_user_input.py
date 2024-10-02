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
    
    # Checks the response is 200 OK
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
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_username_valid_existing_users_populated(self):
    """Tests checking of valid username"""

    valid_data_copy: dict = self.valid_data.copy()
    valid_data_copy['username'] = "user456"

    # Passes valid data and empty list of existing users
    response: Response = check_username(username=self.valid_data['username'],
                                        existing_users=[valid_data_copy])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_username_invalid_non_alphanumeric(self):
    """Tests checking an invalid username with non alphanumeric
    characters in it."""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username='user123?',
                                        existing_users=[])
    
    # Checks the response is as expected
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Username must contain only letters and numbers.")

  def test_check_username_invalid_space(self):
    """Tests checking an invalid username with a space in it."""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username='user 123',
                                        existing_users=[])
    
    # Checks the response is as expected
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Username cannot contain spaces.")

  def test_check_username_invalid_taken(self):
    """Tests checking an invalid username that is already taken by
    another user"""

    # Passes valid data and empty list of existing users
    response: Response = check_username(username=self.valid_data['username'],
                                        existing_users=[self.valid_data])
    
    # Checks the response is as expected
    self.assertEqual(response.status_code, 409)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Username already taken.")
    
    
  ## check_password() Tests ##

  def test_check_password_valid(self):
    """Tests checking a valid password"""

    # Passes valid password
    response: Response = check_password(password=self.valid_data['password'])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_password_invalid_length(self):
    """Tests checking an invalid password that is too short"""

    # Checks the response is as expected
    response: Response = check_password(password="Pass123")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Password must contain a minimum of 8 characters.")

  def test_check_password_invalid_upper(self):
    """Tests checking an invalid password that doesn't contain an upper
    case character."""

    # Checks the response is as expected
    response: Response = check_password(password="pass1234")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Password must contain at least one of both uppercase " \
                     "characters and numbers.")

  def test_check_password_invalid_number(self):
    """Tests checking an invalid password that doesn't contain a
    number."""

    # Checks the response is as expected
    response: Response = check_password(password="Password")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Password must contain at least one of both uppercase " \
                     "characters and numbers.")


  ## check_email() Tests ##

  def test_check_email_valid(self):
    """Tests checking a valid email"""

    # Passes valid email
    response: Response = check_email(email=self.valid_data['email'])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_email_invalid_nodomain(self):
    """Tests an invalid email that is not a valid domain"""

    # Checks the response is as expected
    response: Response = check_email(email="user@example")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Email must be in correct email format. e.g. "\
                     "user@example.com")

  def test_check_email_invalid_noat(self):
    """Tests an invalid password that doesn't contain an @ symbol"""

    # Checks the response is as expected
    response: Response = check_email(email="user.example.com")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'],
                     "Email must be in correct email format. e.g. "\
                     "user@example.com")


  ## check_dob() Tests ##

  def test_check_dob_valid(self):
    """Tests checking a valid dob"""

    # Passes valid DoB
    response: Response = check_dob(dob=self.valid_data['dob'])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_invalid_dob_format(self):
    """Tests checking an invalid DoB that is not in the ISO 8601 format"""

    # Checks the response is as expected
    response = check_dob(dob="01-01-2020")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Date of Birth must be in format: YYYY-MM-DD")

  def test_invalid_dob_nodate(self):
    """Tests checking an invalid DoB that is not a date"""

    # Checks the response is as expected
    response = check_dob(dob="2001")
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                    "Date of Birth must be in format: YYYY-MM-DD")

  def test_invalid_dob_age(self):
    """Tests checking a DoB that would mean the user is under 18"""

    # Checks the response is as expected
    # Sets DoB to today's date
    response = check_dob(dob=date.today().strftime("%Y-%m-%d"))
    self.assertEqual(response.status_code, 403)
    self.assertEqual(json.loads(response.data)['error'], 
                    "User must be at least 18 years old")


  ## check_number() Tests ##

  def test_check_number_valid_ccn(self):
    """Tests checking a valid number"""

    # Passes valid ccn and number of digits in it
    response: Response = check_number(
      num=self.valid_data['credit_card_number'],
      digits=16)
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_number_valid_other(self):
    """Tests checking a valid number"""

    # Passes valid number and number of digits in it
    response: Response = check_number(
      num="12345",
      digits=5)
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 200)

  def test_check_number_invalid_length(self):
    """Tests an invalid number which is not the number of digits passed"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789123456"

    # Passes valid number and number of digits in it
    response: Response = check_number(
      num="1234",
      digits=5)

    # Checks the response is as expected
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 5 numerical digits.")

  def test_check_number_invalid_not_numeric(self):
    """Tests an invalid value which is not numeric"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789a234567"

    # Passes valid number and number of digits in it
    response: Response = check_number(
      num="12a45",
      digits=5)

    # Checks the response is as expected
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 5 numerical digits.")


if __name__ == "__main__":
  unittest.main()