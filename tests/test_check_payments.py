"""
Name: test_check_payments.py
Author: Ryan Gascoigne-Jones

Purpose: Tests the checking functions in check_payments.py.
"""

import unittest
from flask import Response
import json
# Local imports
from utils import check_ccn_registered

class CheckPaymentsTest(unittest.TestCase):
  """Tests the check functions in check_payments.py"""

  def setUp(self):
    """Sets up test data"""

    self.valid_data: dict = {
      "credit_card_number": "1234567891234567",
      "amount": "123"
    }

    self.existing_users: list[dict] = [{
      "username": "user123",
      "password": "Pass1234",
      "email": "user@example.com",
      "dob": "2000-01-01",
      "credit_card_number": "1234567891234567"
    }]


  ## check_ccn_registered() Tests ##

  def test_check_ccn_registered_valid(self):
    """Tests checking a valid registered ccn"""

    # Passes valid data and existing users containing a user with a
    # matching ccn
    response: Response = check_ccn_registered(
      ccn=self.valid_data['credit_card_number'],
      users=self.existing_users,
      amount=self.valid_data['amount'])
    
    # Checks the response is 200 OK
    self.assertEqual(response.status_code, 201)

  def test_check_ccn_registered_invalid_unregistered(self):
    """Tests checking an unregistered ccn"""

    # Changes ccn of the only existing user to a valid but non matching ccn
    new_existing_users: list[dict] = self.existing_users.copy()
    new_existing_users[0]['credit_card_number'] = "1231231231231234"

    # Passes valid data and existing users containing a user with a
    # matching ccn
    response: Response = check_ccn_registered(
      ccn=self.valid_data['credit_card_number'],
      users=new_existing_users,
      amount=self.valid_data['amount'])
    
    # Checks the response is as expected
    self.assertEqual(response.status_code, 404)
    self.assertEqual(json.loads(response.data)['error'],
                      "Credit card number not registered with any user.")