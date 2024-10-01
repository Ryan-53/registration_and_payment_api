"""
Name: check_user_input.py
Author: Ryan Gascoigne-Jones

Purpose: Contains functions which check a request's json body.
"""

from flask import Response
import json
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
# Local Imports
from .utils import check_contains_upper_and_num

def check_username(username: str, existing_users: list[dict]) -> Response:
  """Checks username is valid"""

  # Checks username is alphanumeric
  if not username.isalnum():
    return Response(response=json.dumps({"error": "Username must contain only" \
                      "letters and numbers."}),
                    status=400,
                    content_type="application/json")
  
  # Checks username doesn't contain spaces
  if " " in username:
    return Response(response=json.dumps({"error": "Username cannot contain " \
                      "spaces."}),
                    status=400,
                    content_type="application/json")

  # Checks username doesn't already exist
  for user in existing_users:
    if user['username'] == username:
      return Response(response=json.dumps({"error": "Username already taken."}),
                      status=409,
                      content_type="application/json")

  return Response(status=200)


def check_password(password: str) -> Response:
  """Checks password is valid"""

  # Checks password is at least 8 characters long
  if len(password) < 8:
    return Response(response=json.dumps({"error": "Password must contain a " \
                      "minimum of 8 characters."}),
                    status=400,
                    content_type="application/json")
  
  # Checks password contains both an upper case letter and number
  if not check_contains_upper_and_num(password):
    return Response(response=json.dumps({"error": "Password must contain both" \
                      "upper and lower case characters."}),
                    status=400,
                    content_type="application/json")

  return Response(status=200)


def check_email(email: str) -> Response:
  """Checks email is valid"""

  # Regular expression used for email format
  regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

  # Checks email is in email format
  if not re.match(regex_email, email):
    return Response(response=json.dumps({"error": "Email must be in correct " \
                      "email format. e.g. user@example.com"}),
                    status=400,
                    content_type="application/json")

  return Response(status=200)


def check_dob(dob: str) -> Response:
  """Checks date of birth is valid"""

  # Checks format
  try:
    dob_obj: date = datetime.strptime(dob, "%Y-%m-%d").date()

    # Checks age is above 18
    if dob_obj > (date.today() - relativedelta(years=18)):
      return Response(response=json.dumps({"error": "User must be at least 18" \
                      " years old"}),
                    status=403,
                    content_type="application/json")

  except ValueError:
    return Response(response=json.dumps({"error": "Date of Birth must be in " \
                      "format: YYYY-MM-DD"}),
                    status=400,
                    content_type="application/json")

  return Response(status=200)

def check_number(num: str, digits: int) -> Response:
  """Checks a numerical value is valid"""

  # Checks num is 16 numbers
  if not num.isnumeric() or len(num) != digits:
    return Response(response=json.dumps({"error": "Number must contain " \
                      f"{digits} numerical digits."}),
                    status=400,
                    content_type="application/json")

  return Response(status=200)

      