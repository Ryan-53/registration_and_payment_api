"""
Name: registration_service.py
Author: Ryan Gascoigne-Jones

Purpose: Registration microservice handling user registrations.
"""

from flask import Flask, Response, request, json
from utils import check_username, check_password, check_email, check_dob

app: Flask = Flask(__name__)

@app.route("/users", methods=["POST"])
def register() -> Response:
  """Creates a user based on users JSON input"""

  # Gets json object passed through POST request
  user_input: dict = request.get_json()

  # Checks username
  username: str = user_input["username"]
  username_status: Response = check_username(username=username)
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
  
  return Response(response="User successfully registered",
                  status=201,
                  content_type="application/json")


if __name__ == "__main__":
  app.run(host="localhost", port=3000)