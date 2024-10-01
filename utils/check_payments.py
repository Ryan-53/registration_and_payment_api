"""
Name: check_payments.py
Author: Ryan Gascoigne-Jones

Purpose: Contains functions which check payment information.
"""

from flask import Response
import json

def check_ccn_registered(ccn: str, users: list[dict], amount: str) -> Response:
  """Checks a ccn is registered to a user"""

  # If the ccn is registered to a user return 201 Created for successful
  # payment.
  for user in users:
    if user['ccn'] == ccn:
      return Response(response=json.dumps({"message": f"Payment of {amount} " \
                        "made"}),
                      status=201,
                      content_type="application/json")

  # If ccn is not registered to any user return 404 Not Found
  return Response(response=json.dumps({"error": "Credit card number not " \
                    "registered with any user."}),
                  status=404,
                  content_type="application/json")