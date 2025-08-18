import requests
import json

BASE_URL = "http://localhost:8000"

def test_unified_auth():
    print("🧪 Testing Expedia-Style Unified Authentication")
    print("=" * 50)
    
    # Test 1: New user registration flow
    print("\n📝 Test 1: New User Registration Flow")
    print("-" * 30)
    
    # Step 1: Send OTP for new email
    email = "newuser@example.com"
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": email})
    print(f"Send OTP Response: {response.status_code}")
    if response.status_code == 200:
        otp_data = response.json()
        print(f"OTP Data: {json.dumps(otp_data, indent=2)}")
        
        otp_code = otp_data["otp_code"]
        
        # Step 2: Complete registration with OTP
        registration_data = {
            "email": email,
            "otp_code": otp_code,
            "username": "newuser123",
            "password": "password123",
            "phone": "+1234567890"
        }
        
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json=registration_data)
        print(f"Registration Response: {response.status_code}")
        if response.status_code == 200:
            auth_data = response.json()
            print(f"Auth Data: {json.dumps(auth_data, indent=2)}")
        else:
            print(f"Registration Error: {response.json()}")
    else:
        print(f"Send OTP Error: {response.json()}")
    
    print("\n" + "=" * 50)
    
    # Test 2: Existing user login flow
    print("\n🔐 Test 2: Existing User Login Flow")
    print("-" * 30)
    
    # Step 1: Send OTP for existing email
    existing_email = "newuser@example.com"  # User we just created
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": existing_email})
    print(f"Send OTP Response: {response.status_code}")
    if response.status_code == 200:
        otp_data = response.json()
        print(f"OTP Data: {json.dumps(otp_data, indent=2)}")
        
        otp_code = otp_data["otp_code"]
        
        # Step 2: Login with OTP (no additional info needed)
        login_data = {
            "email": existing_email,
            "otp_code": otp_code
        }
        
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json=login_data)
        print(f"Login Response: {response.status_code}")
        if response.status_code == 200:
            auth_data = response.json()
            print(f"Auth Data: {json.dumps(auth_data, indent=2)}")
        else:
            print(f"Login Error: {response.json()}")
    else:
        print(f"Send OTP Error: {response.json()}")
    
    print("\n" + "=" * 50)
    
    # Test 3: Error cases
    print("\n❌ Test 3: Error Cases")
    print("-" * 20)
    
    # Invalid OTP
    invalid_data = {
        "email": existing_email,
        "otp_code": "999999"
    }
    
    response = requests.post(f"{BASE_URL}/auth/verify-otp", json=invalid_data)
    print(f"Invalid OTP Response: {response.status_code}")
    if response.status_code != 200:
        print(f"Error (Expected): {response.json()}")
    
    # Missing registration info for new user
    new_email = "incomplete@example.com"
    requests.post(f"{BASE_URL}/auth/send-otp", json={"email": new_email})
    
    incomplete_data = {
        "email": new_email,
        "otp_code": "123456"
        # Missing username and password
    }
    
    response = requests.post(f"{BASE_URL}/auth/verify-otp", json=incomplete_data)
    print(f"Incomplete Registration Response: {response.status_code}")
    if response.status_code != 200:
        print(f"Error (Expected): {response.json()}")

def test_frontend_flow():
    """Test the frontend integration flow"""
    print("\n\n🎨 Frontend Integration Flow Example")
    print("=" * 50)
    
    email = "frontend@example.com"
    
    # Step 1: User enters email, frontend calls send-otp
    print(f"\n1. User enters email: {email}")
    response = requests.post(f"{BASE_URL}/auth/send-otp", json={"email": email})
    
    if response.status_code == 200:
        otp_data = response.json()
        user_exists = otp_data.get("user_exists", False)
        action_type = otp_data.get("action_type", "unknown")
        
        print(f"2. System response: user_exists={user_exists}, action_type={action_type}")
        
        if user_exists:
            print("3. Frontend shows: Login form (just OTP input)")
            # Simulate login flow
            login_data = {
                "email": email,
                "otp_code": otp_data["otp_code"]
            }
        else:
            print("3. Frontend shows: Registration form (OTP + username + password)")
            # Simulate registration flow
            login_data = {
                "email": email,
                "otp_code": otp_data["otp_code"],
                "username": "frontenduser",
                "password": "frontendpass123",
                "phone": "+9876543210"
            }
        
        # Step 2: User submits form, frontend calls verify-otp
        print("4. User submits form...")
        response = requests.post(f"{BASE_URL}/auth/verify-otp", json=login_data)
        
        if response.status_code == 200:
            auth_data = response.json()
            print(f"5. Success! Action: {auth_data['action_type']}")
            print(f"   User: {auth_data['user']['username']} ({auth_data['user']['email']})")
            print(f"   Token: {auth_data['access_token']}")
        else:
            print(f"5. Error: {response.json()}")

if __name__ == "__main__":
    print("🚀 Starting Unified Authentication Tests")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    try:
        test_unified_auth()
        test_frontend_flow()
        print("\n✅ All tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
