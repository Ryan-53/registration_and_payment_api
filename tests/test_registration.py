"""
Name: test_registration.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the functioning of the registration endpoint
"""

import unittest
from registration_payment_service import app

class RegistrationTest(unittest.TestCase):
  
  def setUp(self):
    """Set up a test client"""

    app.testing = True
    self.client = app.test_client()

    # Valid input (to be changed by test)
    self.valid_data: dict = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

  def test_valid_registration(self):
    """Tests a completely valid POST request with expected data."""

    # Sends a POST request
    response = self.client.post('/users', json=self.valid_data)
    
    # Checks if the status code is 201 Created
    self.assertEqual(response.status_code, 201)

  ## Username tests

  def test_invalid_username_space(self):
    """Tests an invalid username with a space in it."""

    invalid_data: dict = self.valid_data
    invalid_data['username'] = "user 123"

    response = self.client.post('/users', json=invalid_data)
    
    # Checks if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


  def test_invalid_username_alphanumeric(self):
    """Tests an invalid username with non alphanumeric characters in it."""

    invalid_data: dict = self.valid_data
    invalid_data['username'] = "user123?"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  ## Password tests

  def test_invalid_password_length(self):
    """Tests an invalid password that is too short"""

    invalid_data: dict = self.valid_data
    invalid_data['password'] = "Pass123"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_password_upper(self):
    """Tests an invalid password that doesn't contain an upper case
    character"""

    invalid_data: dict = self.valid_data
    invalid_data['password'] = "pass1234"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_password_number(self):
    """Tests an invalid password that doesn't contain a number"""

    invalid_data: dict = self.valid_data
    invalid_data['password'] = "Password"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  ## Email tests

  def test_invalid_email_nodomain(self):
    """Tests an invalid password that is too short"""

    invalid_data: dict = self.valid_data
    invalid_data['email'] = "user@example"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_email_noat(self):
    """Tests an invalid password that is too short"""

    invalid_data: dict = self.valid_data
    invalid_data['email'] = "user.example.com"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  ## DoB tests

  def test_invalid_dob_format(self):
    """Tests an invalid DoB that is not in the ISO 8601 format"""

    invalid_data: dict = self.valid_data
    invalid_data['dob'] = "01-01-2020"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)

  def test_invalid_dob_nodate(self):
    """Tests an invalid DoB that is not a date"""

    invalid_data: dict = self.valid_data
    invalid_data['dob'] = "2001"

    response = self.client.post('/users', json=invalid_data)
    
    self.assertEqual(response.status_code, 400)

  def test_invalid_dob_age(self):
    """Tests a DoB that would mean the user is under 18"""

    invalid_data: dict = self.valid_data
    # This could cause an error in 18 years but it is better than having an
    # external dependency (time module) in a test.
    invalid_data['dob'] = "2024-01-01"

    # Checks the response's status code is as expected
    response = self.client.post('/users', json=invalid_data)
    self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
  unittest.main()