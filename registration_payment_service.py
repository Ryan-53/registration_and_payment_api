"""
Name: registration_service.py
Author: Ryan Gascoigne-Jones

Purpose: Service handling user registrations and payments
"""

from flask import Flask, Response, request, json
from utils import check_username, check_password, check_email, check_dob, check_ccn

app: Flask = Flask(__name__)

@app.route("/users", methods=["POST"])
def register() -> Response:
  """Creates a user based on users JSON input"""

  # Gets json object passed through POST request
  user_input: dict = request.get_json()

  # Checks username
  username: str = user_input["username"]
  username_status: Response = check_username(username=username)
  # Returns error status if an invalid username has been entered
  if username_status.status_code != 200:
    return username_status
  
  # Checks password
  password: str = user_input["password"]
  password_status: Response = check_password(password=password)
  if password_status.status_code != 200:
    return password_status
  
  # Checks email
  email: str = user_input["email"]
  email_status: Response = check_email(email=email)
  if email_status.status_code != 200:
    return email_status
  
  # Checks DoB
  dob: str = user_input["dob"]
  dob_status: Response = check_dob(dob=dob)
  if dob_status.status_code != 200:
    return dob_status

  # Checks credit card number
  ccn_status: Response
  ccn: str
  # Try statement in case the ccn hasn't been input (as it is optional)
  try:
    ccn = user_input["credit_card_number"]
    ccn_status = check_ccn(ccn=ccn)
    if ccn_status.status_code != 200:
      return ccn_status
  # Leaves ccn empty if no ccn has been input
  except:
    ccn = ""
  
  return Response(response="User successfully registered",
                  status=201,
                  content_type="application/json")


if __name__ == "__main__":
  app.run(host="localhost", port=3000)