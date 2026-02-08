#!/usr/bin/env python3
"""
Complete Signup Flow Test
Tests registration from frontend API call through to database verification
"""

import requests
import sys
from datetime import datetime
from sqlmodel import Session, select

# Add backend to path
sys.path.insert(0, '/mnt/e/agentic_ai/todo-phase-3/backend')

from src.database import engine
from src.models.user import User

def test_complete_signup_flow():
    """Test complete signup flow and verify in database"""

    # Generate unique test email
    timestamp = int(datetime.now().timestamp())
    test_email = f"testuser{timestamp}@example.com"
    test_password = "SecurePass123!"

    print("=" * 60)
    print("COMPLETE SIGNUP FLOW TEST")
    print("=" * 60)
    print(f"\n📧 Test Email: {test_email}")
    print(f"🔒 Test Password: {test_password}")

    # Step 1: Test Backend Direct Registration
    print("\n" + "=" * 60)
    print("STEP 1: Direct Backend Registration")
    print("=" * 60)

    backend_url = "http://localhost:8000/auth/register"
    payload = {
        "email": test_email,
        "password": test_password
    }

    print(f"\n📤 POST {backend_url}")
    print(f"📦 Payload: {payload}")

    try:
        response = requests.post(backend_url, json=payload, timeout=10)
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response: {response.json()}")

        if response.status_code == 200 or response.status_code == 201:
            token = response.json().get('access_token')
            print(f"\n🎫 JWT Token Received: {token[:50]}...")
        else:
            print(f"\n❌ Registration failed: {response.json()}")
            return False

    except Exception as e:
        print(f"\n❌ Backend request failed: {e}")
        return False

    # Step 2: Verify in Database
    print("\n" + "=" * 60)
    print("STEP 2: Database Verification")
    print("=" * 60)

    try:
        with Session(engine) as session:
            # Query for the user
            statement = select(User).where(User.email == test_email)
            user = session.exec(statement).first()

            if user:
                print(f"\n✅ USER FOUND IN DATABASE!")
                print(f"\n📊 User Details:")
                print(f"   ID: {user.id}")
                print(f"   Email: {user.email}")
                print(f"   Password Hash: {user.hashed_password[:50]}...")
                print(f"   Created At: {user.created_at}")
                print(f"   Updated At: {user.updated_at}")

                # Verify password is hashed
                if user.hashed_password.startswith('$2b$'):
                    print(f"\n✅ Password properly hashed with bcrypt")
                else:
                    print(f"\n⚠️  Password hash format unexpected: {user.hashed_password[:20]}...")

            else:
                print(f"\n❌ USER NOT FOUND IN DATABASE!")
                print(f"   Email searched: {test_email}")
                return False

    except Exception as e:
        print(f"\n❌ Database query failed: {e}")
        return False

    # Step 3: List All Users
    print("\n" + "=" * 60)
    print("STEP 3: All Users in Database")
    print("=" * 60)

    try:
        with Session(engine) as session:
            users = session.exec(select(User)).all()
            print(f"\n📋 Total Users: {len(users)}")
            print("\n👥 User List:")
            for i, u in enumerate(users, 1):
                print(f"   {i}. {u.email} (ID: {u.id}, Created: {u.created_at})")

    except Exception as e:
        print(f"\n❌ Failed to list users: {e}")

    # Step 4: Test Login with New User
    print("\n" + "=" * 60)
    print("STEP 4: Test Login with New User")
    print("=" * 60)

    login_url = "http://localhost:8000/auth/signin"
    login_payload = {
        "email": test_email,
        "password": test_password
    }

    print(f"\n📤 POST {login_url}")
    print(f"📦 Payload: {login_payload}")

    try:
        response = requests.post(login_url, json=login_payload, timeout=10)
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📥 Response: {response.json()}")

        if response.status_code == 200:
            print(f"\n✅ LOGIN SUCCESSFUL!")
            print(f"🎫 New JWT Token: {response.json().get('access_token', '')[:50]}...")
        else:
            print(f"\n❌ Login failed: {response.json()}")
            return False

    except Exception as e:
        print(f"\n❌ Login request failed: {e}")
        return False

    # Final Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"\n✅ Registration: SUCCESS")
    print(f"✅ Database Verification: SUCCESS")
    print(f"✅ User in Database: {test_email}")
    print(f"✅ Login: SUCCESS")
    print(f"\n🎉 ALL TESTS PASSED!")

    return True

if __name__ == "__main__":
    success = test_complete_signup_flow()
    sys.exit(0 if success else 1)
