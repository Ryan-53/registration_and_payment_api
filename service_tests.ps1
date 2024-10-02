# Define the base URLs
$userUrl = "http://localhost:3000/users"
$paymentUrl = "http://localhost:3000/payments"

# Define headers as a dictionary
$headers = @{
  "Content-Type" = "application/json"
}

# Test Case 1: Get users where filter returns no users due to no users
# in system (e.g., CreditCard=Yes with no CCNs)
Write-Host "Test Case 1: Get users where filter returns no users"
Invoke-WebRequest -Uri $userUrl"?CreditCard=Yes" `
-Method GET `
-Headers $headers
Write-Host "--------------------------------------"

# Test Case 2: Valid registration request with all required fields
Write-Host "Test Case 2: Valid Registration (With Credit Card)"
Invoke-WebRequest -Uri $userUrl `
-Method POST `
-Headers $headers `
-Body '{"username": "user123", "password": "Pass1234", "email": "user123@example.com", "dob": "2000-01-01", "credit_card_number": "1234567891234567"}'
Write-Host "--------------------------------------"

# Test Case 3: Valid registration request without Credit Card
Write-Host "Test Case 3: Valid Registration (Without Credit Card)"
Invoke-WebRequest -Uri $userUrl `
-Method POST `
-Headers $headers `
-Body '{"username": "user456", "password": "Pass5678", "email": "user456@example.com", "dob": "1995-05-20"}'
Write-Host "--------------------------------------"

# Test Case 4: Invalid registration (username already exists)
Write-Host "Test Case 4: Invalid Registration (Username already exists)"
Invoke-WebRequest -Uri $userUrl `
-Method POST `
-Headers $headers `
-Body '{"username": "user123", "password": "Pass9999", "email": "user999@example.com", "dob": "1995-05-20", "credit_card_number": "9876543210987654"}'
Write-Host "--------------------------------------"

# Test Case 5: Invalid registration (missing required fields)
Write-Host "Test Case 5: Invalid Registration (Missing Required Fields)"
Invoke-WebRequest -Uri $userUrl `
-Method POST `
-Headers $headers `
-Body '{"username": "user789", "email": "user789@example.com"}' # Missing password and dob
Write-Host "--------------------------------------"

# Test Case 6: Invalid registration (user under 18)
Write-Host "Test Case 6: Invalid Registration (User Under 18)"
Invoke-WebRequest -Uri $userUrl `
-Method POST `
-Headers $headers `
-Body '{"username": "younguser", "password": "Pass1234", "email": "younguser@example.com", "dob": "2010-01-01"}'
Write-Host "--------------------------------------"

# Test Case 7: Get all users without a filter
Write-Host "Test Case 7: Get all users (No filter)"
Invoke-WebRequest -Uri $userUrl `
-Method GET `
-Headers $headers
Write-Host "--------------------------------------"

# Test Case 8: Get users with credit card filter (CreditCard=Yes)
Write-Host "Test Case 8: Get users with CreditCard=Yes"
Invoke-WebRequest -Uri $userUrl"?CreditCard=Yes" `
-Method GET `
-Headers $headers
Write-Host "--------------------------------------"

# Test Case 9: Get users with credit card filter (CreditCard=No)
Write-Host "Test Case 9: Get users with CreditCard=No"
Invoke-WebRequest -Uri $userUrl"?CreditCard=No" `
-Method GET `
-Headers $headers
Write-Host "--------------------------------------"

# Test Case 10: Valid payment request (existing user with credit card)
Write-Host "Test Case 10: Valid payment request (existing user)"
Invoke-WebRequest -Uri $paymentUrl `
-Method POST `
-Headers $headers `
-Body '{"credit_card_number": "1234567891234567", "amount": "500"}'
Write-Host "--------------------------------------"

# Test Case 11: Invalid payment request (non-existing credit card)
Write-Host "Test Case 11: Invalid payment request (non-existing credit card)"
Invoke-WebRequest -Uri $paymentUrl `
-Method POST `
-Headers $headers `
-Body '{"credit_card_number": "1111222233334444", "amount": "500"}'
Write-Host "--------------------------------------"

# Test Case 12: Invalid payment request (missing required fields)
Write-Host "Test Case 12: Invalid payment request (Missing Required Fields)"
Invoke-WebRequest -Uri $paymentUrl `
-Method POST `
-Headers $headers `
-Body '{"credit_card_number": "1234567891234567"}' # Missing amount
Write-Host "--------------------------------------"
