# 🔐 Authentication API Summary

## 📋 **Available Endpoints (Simplified)**

### **Base URL:** `http://localhost:8000/auth`

---

## 🎯 **Only 2 Endpoints Needed**

### 1️⃣ **Send OTP**
```
POST /auth/send-otp
```

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent to user@example.com for login/registration",
  "email": "user@example.com",
  "otp_code": "123456",
  "expires_in_minutes": 10,
  "action_type": "login" | "registration",
  "user_exists": true | false
}
```

### 2️⃣ **Verify OTP**
```
POST /auth/verify-otp
```

**Request:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "user",
    "email": "user@example.com",
    "phone": null,
    "is_verified": true
  },
  "action_type": "login" | "registration",
  "message": "Login successful" | "Auto-registration and login successful"
}
```

---

## 🚀 **How It Works**

### **For Existing Users:**
1. **Send OTP** → Returns `"user_exists": true, "action_type": "login"`
2. **Verify OTP** → Logs user in immediately

### **For New Users:**
1. **Send OTP** → Returns `"user_exists": false, "action_type": "registration"`
2. **Verify OTP** → Auto-creates account and logs user in

---

## ✅ **Features**

- **Unified Flow**: Same endpoints for login and registration
- **Auto-Registration**: New users are automatically registered
- **Username Generation**: Auto-generated from email (e.g., `john.doe` from `john.doe@gmail.com`)
- **JWT Tokens**: Secure authentication with access tokens
- **Static OTP**: Development uses `123456` (10-minute expiry)
- **Email Only**: No need for username, password, or phone during signup

---

## 🧪 **Test Examples**

### **New User Registration + Login:**
```bash
# Step 1: Send OTP
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"email": "newuser@example.com"}'

# Response: {"user_exists": false, "action_type": "registration", "otp_code": "123456"}

# Step 2: Verify OTP (auto-creates account)
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"email": "newuser@example.com", "otp_code": "123456"}'

# Response: User created and logged in with JWT token
```

### **Existing User Login:**
```bash
# Step 1: Send OTP
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"email": "existing@example.com"}'

# Response: {"user_exists": true, "action_type": "login", "otp_code": "123456"}

# Step 2: Verify OTP
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"email": "existing@example.com", "otp_code": "123456"}'

# Response: User logged in with JWT token
```

---

## 🔧 **Python Test Script**

```python
import requests

BASE_URL = "http://localhost:8000"

def test_auth_flow(email):
    print(f"Testing auth flow for: {email}")
    
    # Step 1: Send OTP
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": email})
    print(f"Send OTP Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"User exists: {data['user_exists']}")
        print(f"Action type: {data['action_type']}")
        otp_code = data['otp_code']
        
        # Step 2: Verify OTP
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json={
            "email": email,
            "otp_code": otp_code
        })
        print(f"Verify OTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Action: {data['action_type']}")
            print(f"Token: {data['access_token'][:50]}...")
            print(f"User: {data['user']['username']}")
    
    print("-" * 50)

# Test both new and existing users
test_auth_flow("newuser@example.com")
test_auth_flow("newuser@example.com")  # Second time should be login
```

---

## 📊 **Authentication Flow**

```
User enters email
       ↓
   Send OTP API
       ↓
System checks if user exists
       ↓
   ┌─────────────────┬─────────────────┐
   │   User Exists   │  User New       │
   │   (Login)       │  (Registration) │
   └─────────────────┴─────────────────┘
       ↓                     ↓
User enters OTP          User enters OTP
       ↓                     ↓
  Verify OTP API       Verify OTP API
       ↓                     ↓
   Login Success        Auto-register + Login
       ↓                     ↓
   JWT Token            JWT Token
```

🎉 **Simple, secure, and Expedia-like authentication!**
