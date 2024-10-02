"""
Name: registration_payment_service.py
Author: Ryan Gascoigne-Jones

Purpose: Service handling user registrations and payments
"""

from flask import Flask, Response, request, json
from utils import check_username, check_password, check_email, check_dob, \
  check_number, check_ccn_registered, check_input_present

app: Flask = Flask(__name__)

users: list[dict] = []

@app.route("/users", methods=["POST"])
def register() -> Response:
  """Creates a user based on users JSON input"""

  # Gets json object passed through POST request
  user_input: dict = request.get_json()

  # Checks if there are any absent values (except ccn)
  input_check_response: Response = check_input_present(
    user_input=user_input.copy(),
    expected=["username", "password", "email", "dob"])
  if input_check_response.status_code != 200:
    return input_check_response

  # Checks username
  username: str = user_input["username"]
  username_status: Response = check_username(username=username,
                                             existing_users=users)
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
  # Try statement in case the ccn hasn't been input (as it is optional)
  try:
    ccn: str = user_input["credit_card_number"]
    ccn_status: Response = check_number(num=ccn, digits=16)
    if ccn_status.status_code != 200:
      return ccn_status
    
    # Creates new_user dict to add to users list
    new_user: dict = {
      'username': username,
      'password': password,
      'email': email,
      'dob': dob,
      'credit_card_number': ccn
    }

  # Creates new_user dict with no ccn
  except:
    new_user: dict = {
      'username': username,
      'password': password,
      'email': email,
      'dob': dob
    }

  # Creates user (adds to store)
  users.append(new_user)
  
  # Returns 201 Created along with details of the newly registered user
  return Response(response=json.dumps({
                    "message": "User successfully registered",
                    "user": new_user
                  }),
                  status=201,
                  content_type="application/json")


@app.route("/users", methods=["GET"])
def get_users() -> Response:

  # Gets credit card filter from query parameter
  cc_filter = request.args.get('CreditCard')
  filtered_users: list[dict] = []

  # If cc filter is "Yes" return all users with a ccn
  if cc_filter == "Yes":
    for user in users:
      # Checks if each user has a ccn
      if user['credit_card_number']:
        filtered_users.append(user)

  # If cc filter is "No" return all users without a ccn
  elif cc_filter == "No":
    for user in users:
      if not user['credit_card_number']:
        filtered_users.append(user)

  # If a cc filter was not given, return all users
  else:
    filtered_users = users

  # If there is no users for the given filter return 204 No Content
  if filtered_users == []:
    return Response(status=204)

  # Returns list of users for chosen filter along with 200 OK
  return Response(response=json.dumps(filtered_users),
                  status=200,
                  content_type="application/json")


@app.route("/payments", methods=["POST"])
def make_payment() -> Response:
  """Checks payment values are correct, if so returning 201 Created"""

  # Gets json object passed through POST request
  user_input: dict = request.get_json()

  # Checks if there are any absent values
  input_check_response: Response = check_input_present(
    user_input=user_input.copy(),
    expected=["credit_card_number", "amount"])
  if input_check_response.status_code != 200:
    return input_check_response
  
  # Checks credit card number is valid
  ccn: str = user_input["credit_card_number"]
  ccn_status: Response = check_number(num=ccn, digits=16)
  if ccn_status.status_code != 200:
    return ccn_status

  # Checks amount is valid
  amount: str = user_input["amount"]
  amount_status: Response = check_number(num=amount, digits=3)
  if amount_status.status_code != 200:
    return amount_status
  
  # Checks credit card number is registered to a user in system
  return check_ccn_registered(ccn=ccn, users=users, amount=amount)


if __name__ == "__main__":
  app.run(host="localhost", port=3000)