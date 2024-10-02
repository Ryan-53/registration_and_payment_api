"""
Name: test_users.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the functioning of the users endpoint.
"""

import unittest
from unittest.mock import patch
from registration_payment_service import app
from datetime import date
import json

### register() tests

class RegistrationTest(unittest.TestCase):
  """Tests the register() mapping function"""
  
  def setUp(self):
    """Set up a test client and mock data"""

    app.testing = True
    self.client = app.test_client()

    # Valid input (to be changed by test)
    self.valid_data: dict = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567891234567"
    }


  ## Normal valid register test ##

  def test_valid_registration(self):
    """Tests a completely valid POST request with expected data."""

    # Mocks the users list
    with patch('registration_payment_service.users', new=[]) as mock_users:

      # Sends a POST request
      response = self.client.post('/users', json=self.valid_data)
      
      # Checks if the status code is 201 Created
      self.assertEqual(response.status_code, 201)
      # Checks the data of the user created and saved matches with the
      # data sent in request
      self.assertEqual(json.loads(response.data)['user'], self.valid_data)


  ## Username tests ##

  def test_invalid_username_space(self):
    """Tests an invalid username with a space in it."""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['username'] = "user 123"

    response = self.client.post('/users', json=invalid_data)
    
    # Checks if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)

  def test_invalid_username_non_alphanumeric(self):
    """Tests an invalid username with non alphanumeric characters in
    it."""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['username'] = "user123?"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_username_taken(self):
    """Tests an invalid username that is already taken by another
    user"""

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', new=[]) as mock_users:

      # Checks the response's status code is 201 Created for the first
      # creation and 409 Conflict when the same user is attempted to be
      # created again.
      response = self.client.post('/users', json=self.valid_data)
      self.assertEqual(response.status_code, 201)
      response = self.client.post('/users', json=self.valid_data)
      self.assertEqual(response.status_code, 409)

      # Checks that only 1 instance of the user was added to the mocked
      # users list.
      self.assertEqual(len(mock_users), 1)
      self.assertEqual(mock_users[0]["username"], self.valid_data["username"])


  ## Password tests ##

  def test_invalid_password_length(self):
    """Tests an invalid password that is too short"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "Pass123"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_password_upper(self):
    """Tests an invalid password that doesn't contain an upper case
    character."""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "pass1234"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_password_number(self):
    """Tests an invalid password that doesn't contain a number"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['password'] = "Password"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)


  ## Email tests ##

  def test_invalid_email_nodomain(self):
    """Tests an invalid email that is not a valid domain"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['email'] = "user@example"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_email_noat(self):
    """Tests an invalid password that doesn't contain an @ symbol"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['email'] = "user.example.com"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)


  ## DoB tests ##

  def test_invalid_dob_format(self):
    """Tests an invalid DoB that is not in the ISO 8601 format"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['dob'] = "01-01-2020"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_dob_nodate(self):
    """Tests an invalid DoB that is not a date"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['dob'] = "2001"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_dob_age(self):
    """Tests a DoB that would mean the user is under 18"""

    invalid_data: dict = self.valid_data.copy()
    # Sets DoB to todays date
    invalid_data['dob'] = date.today().strftime("%Y-%m-%d")

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 403)


  ## Credit card number tests ##

  def test_invalid_ccn_length(self):
    """Tests an invalid credit card number which is not 16 digits"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789123456"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_ccn_not_numeric(self):
    """Tests an invalid credit card number which is not numeric"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789a234567"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 16 numerical digits.")

  def test_valid_ccn_none(self):
    """Tests passing no credit card number"""

    # Removes ccn from valid_data dict copy
    valid_data: dict = self.valid_data.copy()
    valid_data.pop('credit_card_number')

    # Checks the response's status code is as expected (201 Created)
    response = self.client.post('/users', json=valid_data)
    self.assertEqual(response.status_code, 201)


  ## User creation test ##

  def test_user_creation(self):
    """Tests the creation of a user during valid registration"""

    # Mocks the users list
    with patch('registration_payment_service.users', new=[]) as mock_users:

      # Checks the response's status code is as expected (201 Created)
      response = self.client.post('/users', json=self.valid_data)
      self.assertEqual(response.status_code, 201)

      # Checks if the user was added to the mocked users list
      self.assertEqual(len(mock_users), 1)
      self.assertEqual(mock_users[0]["username"], self.valid_data["username"])

  def test_user_creation_multiple(self):
    """Tests the creation of 2 users with valid registrations"""

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', new=[]) as mock_users:

      second_valid_data: dict = self.valid_data.copy()
      second_valid_data['username'] = 'user456'

      # Checks the response's status code is as expected for both user
      # creations (201 Created).
      response = self.client.post('/users', json=self.valid_data)
      self.assertEqual(response.status_code, 201)
      response = self.client.post('/users', json=second_valid_data)
      self.assertEqual(response.status_code, 201)

      # Checks if both users were added to the mocked users list
      self.assertEqual(len(mock_users), 2)
      self.assertEqual(mock_users[0]["username"], self.valid_data["username"])
      self.assertEqual(mock_users[1]["username"],
                       second_valid_data["username"])


  ## Absent value test ##

  def test_register_absent_value(self):
    """Tests the handling of a request with absent required values"""

    # Removes email from valid_data dict copy
    invalid_data: dict = self.valid_data.copy()
    invalid_data.pop('email')

    # Checks the response's status code is 400 Bad Request
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "email must be provided.")



### get_users() tests

class GetUsersTest(unittest.TestCase):
  """Tests the get_users() mapping function"""

  def setUp(self):
    """Set up a test client and mock data"""

    app.testing = True
    self.client = app.test_client()

    self.users = [
      {"username": "user1", "credit_card_number": "1234567812345678"},
      {"username": "user2", "credit_card_number": ""},
      {"username": "user3", "credit_card_number": "8765432187654321"}
    ]

  def test_get_users_cc_filter_yes(self):
    """Tests the GET /users endpoint with cc filter of 'Yes' """

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', self.users):

      # Send GET request with a CreditCard=Yes query
      response = self.client.get('/users?CreditCard=Yes')
      self.assertEqual(response.status_code, 200)

      # Parse the json response body
      filtered_users = json.loads(response.data)

      # Check that only the two users without a ccn are returned
      self.assertEqual(len(filtered_users), 2)
      self.assertIn(
        {"username": "user1", "credit_card_number": "1234567812345678"},
        filtered_users)
      self.assertIn(
        {"username": "user3", "credit_card_number": "8765432187654321"},
        filtered_users)

  def test_get_users_cc_filter_no(self):
    """Tests the GET /users endpoint with cc filter of 'No' """

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', self.users):

      # Send GET request with a CreditCard=Yes query
      response = self.client.get('/users?CreditCard=No')
      self.assertEqual(response.status_code, 200)

      # Parse the json response body
      filtered_users = json.loads(response.data)

      # Check that the only user without a ccn is returned
      self.assertEqual(len(filtered_users), 1)
      self.assertIn({"username": "user2", "credit_card_number": ""},
                    filtered_users)

  def test_get_users_cc_filter_none(self):
    """Tests the GET /users endpoint with no cc filter"""

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', self.users):

      # Send GET request with a CreditCard=Yes query
      response = self.client.get('/users')
      self.assertEqual(response.status_code, 200)

      # Parse the json response body
      filtered_users = json.loads(response.data)

      # Check that all users are returned
      self.assertEqual(len(filtered_users), 3)
      self.assertEqual(self.users, filtered_users)


if __name__ == "__main__":
  unittest.main()