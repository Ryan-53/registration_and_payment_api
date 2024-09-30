"""
Name: test_registration.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the functioning of the registration endpoint
"""

import unittest
from registration_service import app

class RegistrationTest(unittest.TestCase):
  
  def setUp(self):
    """Set up a test client"""

    app.testing = True
    self.client = app.test_client()

  def test_valid_registration(self):
    """Tests a completely valid POST request with expected data."""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 201 Created
    self.assertEqual(response.status_code, 201)

  ## Username tests

  def test_invalid_username_space(self):
    """Tests an invalid username with a space in it."""

    # Valid input
    valid_data = {
      "username": "user 123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


  def test_invalid_username_alphanumeric(self):
    """Tests an invalid username with non alphanumeric characters in it."""

    # Valid input
    valid_data = {
      "username": "user123?",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)

  ## Password tests

  def test_invalid_password_length(self):
    """Tests an invalid password that is too short"""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "Pass123",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


  def test_invalid_password_upper(self):
    """Tests an invalid password that doesn't contain an upper case
    character"""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


  def test_invalid_password_number(self):
    """Tests an invalid password that doesn't contain a number"""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "Password",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)

  ## Email tests

  def test_invalid_email_nodomain(self):
    """Tests an invalid password that is too short"""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


  def test_invalid_email_noat(self):
    """Tests an invalid password that is too short"""

    # Valid input
    valid_data = {
      "username": "user123",
      "password": "Pass1234",
      "email": "user.example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567812345678"
    }

    # Send a POST request
    response = self.client.post('/users', json=valid_data)
    
    # Check if the status code is 400 Bad Request
    self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
  unittest.main()