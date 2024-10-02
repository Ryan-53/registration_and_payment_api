"""
Name: test_payments.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the functioning of the payments endpoint.
"""

import unittest
from unittest.mock import patch
from registration_payment_service import app
import json

## make_payment() tests

class MakePaymentTest(unittest.TestCase):
  """Tests the make_payment() mapping function"""

  def setUp(self):
    """Set up a test client and mock data"""

    app.testing = True
    self.client = app.test_client()

    self.valid_data: dict = {
      "credit_card_number": "1234567891234567",
      "amount": "123"
    }

    self.mock_users: list[dict] = [{
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567891234567"
    }]


  ## Valid payment test ##

  def test_valid_payment(self):
    """Tests a valid POST request to /payments endpoint"""

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', self.mock_users):

      response = self.client.post('/payments', json=self.valid_data)
      self.assertEqual(response.status_code, 201)
      self.assertEqual(json.loads(response.data)['message'],
                       f"Payment of {self.valid_data['amount']} made.")


  ## Credit card number tests ##

  def test_invalid_ccn_length(self):
    """Tests an invalid credit card number which is not 16 digits"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789123456"

    # Checks the response's status code is as expected (400 Bad Request)
    response = self.client.post('/payments', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 16 numerical digits.")

  def test_invalid_ccn_not_numeric(self):
    """Tests an invalid credit card number which is not numeric"""

    invalid_data: dict = self.valid_data.copy()
    invalid_data['credit_card_number'] = "123456789a234567"

    # Checks the response's status code is as expected (400 Bad Request)
    response = self.client.post('/payments', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 16 numerical digits.")

  def test_valid_ccn_none(self):
    """Tests passing no credit card number"""

    valid_data: dict = self.valid_data.copy()
    valid_data.pop('credit_card_number')

    # Checks the response's status code is as expected (400 Bad Request)
    response = self.client.post('/payments', json=valid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "credit_card_number must be provided.")

  def test_invalid_cnn_unregistered(self):
    """Tests a payments POST request using an unregistered ccn"""

    # Mocks the users list (exists within this test case only)
    with patch('registration_payment_service.users', self.mock_users):

      # Changes ccn to a valid but unregistered ccn
      invalid_data: dict = self.valid_data.copy()
      invalid_data['credit_card_number'] = "1234567891234568"

      response = self.client.post('/payments', json=invalid_data)
      self.assertEqual(response.status_code, 404)
      self.assertEqual(json.loads(response.data)['error'],
                       "Credit card number not registered with any user.")


  ## Amount value tests ##

  def test_invalid_amount_length(self):

    invalid_data: dict = self.valid_data.copy()
    invalid_data['amount'] = "12"

    # Checks the response's status code is as expected (400 Bad Request)
    response = self.client.post('/payments', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "Number must contain 3 numerical digits.")
    
    
  ## Absent value test ##

  def test_payments_absent_value(self):
    """Tests the handling of a request with absent required values"""

    # Removes email from valid_data dict copy
    invalid_data: dict = self.valid_data.copy()
    invalid_data.pop('amount')

    # Checks the response's status code is 400 Bad Request
    response = self.client.post('/payments', json=invalid_data)
    self.assertEqual(response.status_code, 400)
    self.assertEqual(json.loads(response.data)['error'], 
                     "amount must be provided.")
    

if __name__ == "__main__":
  unittest.main()