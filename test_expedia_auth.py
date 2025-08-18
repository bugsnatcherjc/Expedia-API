#!/usr/bin/env python3

# Test script for Expedia-style OTP Authentication System

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_expedia_style_auth():
    print("🔐 Testing Expedia-Style OTP Authentication System")
    print("=" * 70)
    
    # Test data
    test_email = "john.doe@example.com"
    test_phone = "+1234567890"
    test_username = "johndoe"
    test_password = "password123"
    static_otp = "123456"  # Our static OTP
    
    print("\n🚀 SCENARIO 1: NEW USER SIGNUP WITH OTP")
    print("-" * 50)
    
    # Step 1: Send OTP for signup
    print("1️⃣ Sending OTP for new user signup...")
    signup_request = {
        "email": test_email,
        "phone": test_phone
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup/send-otp", json=signup_request)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        otp_data = response.json()
        print(f"   ✅ OTP sent to: {otp_data['email']}")
        print(f"   🔑 OTP Code: {otp_data['otp_code']} (expires in {otp_data['expires_in_minutes']} minutes)")
    else:
        print(f"   ❌ Error: {response.text}")
        return
    
    print()
    
    # Step 2: Complete signup with OTP
    print("2️⃣ Completing signup with OTP verification...")
    complete_signup = {
        "email": test_email,
        "username": test_username,
        "password": test_password,
        "otp_code": static_otp
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup/complete", json=complete_signup)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"   ✅ User created successfully!")
        print(f"   👤 User ID: {user_data['id']}")
        print(f"   📧 Email: {user_data['email']}")
        print(f"   📱 Phone: {user_data['phone']}")
        print(f"   ✅ Verified: {user_data['is_verified']}")
    else:
        print(f"   ❌ Error: {response.text}")
        return
    
    print()
    print("\n🔄 SCENARIO 2: EXISTING USER LOGIN WITH OTP")
    print("-" * 50)
    
    # Step 1: Send OTP for login
    print("1️⃣ Sending OTP for existing user login...")
    login_request = {
        "email": test_email
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/send-otp", json=login_request)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        otp_data = response.json()
        print(f"   ✅ OTP sent to: {otp_data['email']}")
        print(f"   🔑 OTP Code: {otp_data['otp_code']} (expires in {otp_data['expires_in_minutes']} minutes)")
    else:
        print(f"   ❌ Error: {response.text}")
        return
    
    print()
    
    # Step 2: Login with OTP
    print("2️⃣ Logging in with OTP verification...")
    login_with_otp = {
        "email": test_email,
        "otp_code": static_otp
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/verify-otp", json=login_with_otp)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        login_data = response.json()
        print(f"   ✅ Login successful!")
        print(f"   🎫 Token: {login_data['token']}")
        print(f"   👤 User: {login_data['user']['username']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    print()
    print("\n❌ SCENARIO 3: ERROR CASES")
    print("-" * 50)
    
    # Test duplicate signup
    print("1️⃣ Testing duplicate email signup...")
    response = requests.post(f"{BASE_URL}/auth/signup/send-otp", json=signup_request)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected: {response.json()['detail']}")
    else:
        print(f"   ❌ Unexpected response: {response.text}")
    
    print()
    
    # Test login with non-existent email
    print("2️⃣ Testing login with non-existent email...")
    fake_login = {"email": "nonexistent@example.com"}
    response = requests.post(f"{BASE_URL}/auth/login/send-otp", json=fake_login)
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print(f"   ✅ Correctly rejected: {response.json()['detail']}")
    else:
        print(f"   ❌ Unexpected response: {response.text}")
    
    print()
    
    # Test invalid OTP
    print("3️⃣ Testing invalid OTP...")
    invalid_otp = {
        "email": test_email,
        "otp_code": "999999"
    }
    response = requests.post(f"{BASE_URL}/auth/login/verify-otp", json=invalid_otp)
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected: {response.json()['detail']}")
    else:
        print(f"   ❌ Unexpected response: {response.text}")
    
    print("\n" + "=" * 70)
    print("✨ EXPEDIA-STYLE AUTHENTICATION SUMMARY")
    print("=" * 70)
    print("🔄 SIGNUP FLOW:")
    print("   1. POST /auth/signup/send-otp     → Send OTP to email/phone")
    print("   2. POST /auth/signup/complete     → Complete signup with OTP")
    print()
    print("🔄 LOGIN FLOW:")
    print("   1. POST /auth/login/send-otp      → Send OTP to registered email/phone")
    print("   2. POST /auth/login/verify-otp    → Login with OTP verification")
    print()
    print("🔑 STATIC OTP (Development): 123456")
    print("⏰ OTP Expiry: 10 minutes")
    print("✅ Email verification: Automatic upon successful OTP verification")

if __name__ == "__main__":
    test_expedia_style_auth()
