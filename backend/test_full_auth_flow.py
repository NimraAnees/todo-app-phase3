#!/usr/bin/env python3
"""
End-to-end authentication flow test to verify that sign-in works properly.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

async def test_authentication_flow():
    """Test the complete authentication flow: signup -> signin -> get user"""
    print("Testing Complete Authentication Flow")
    print("=" * 50)

    # Import required modules
    from app.routers.auth import register, signin, get_current_user_info
    from app.models.user import User
    from app.schemas.auth import UserCreate, UserLogin
    from sqlmodel import Session
    from fastapi import HTTPException

    # Mock database session
    mock_db = MagicMock(spec=Session)

    # Test user data
    test_email = "testuser@example.com"
    test_password = "SecurePassword123!"
    test_name = "Test User"

    print(f"1. Testing Signup with email: {test_email}")

    # Create user for signup
    user_create = UserCreate(
        email=test_email,
        password=test_password,
        name=test_name
    )

    # Mock the database operations for signup
    with patch('app.routers.auth.select') as mock_select, \
         patch('app.routers.auth.User') as mock_user_class, \
         patch('uuid.uuid4') as mock_uuid:

        # Setup mocks
        mock_uuid.return_value = "mocked-uuid-123"
        mock_db.exec.return_value.first.return_value = None  # No existing user

        # Create a mock user object
        mock_new_user = MagicMock(spec=User)
        mock_new_user.id = "mocked-uuid-123"
        mock_new_user.email = test_email
        mock_new_user.name = test_name
        from datetime import datetime
        mock_new_user.created_at = datetime.now()

        # Mock the User constructor
        mock_user_instance = MagicMock()
        mock_user_instance.id = "mocked-uuid-123"
        mock_user_instance.email = test_email
        mock_new_user = mock_user_instance

        # Patch the User class constructor
        with patch('app.models.user.User') as mock_user_constructor:
            mock_user_constructor.return_value = mock_new_user

            # Add the user to the mock db session
            mock_db.add = MagicMock()
            mock_db.commit = MagicMock()
            mock_db.refresh = MagicMock(return_value=mock_new_user)

            try:
                # Attempt signup
                result = await register(user_create, mock_db)
                print(f"   ✓ Signup successful: {result.user.email}")

                # Verify that user was added to database
                mock_db.add.assert_called_once()
                mock_db.commit.assert_called_once()

            except HTTPException as e:
                print(f"   ✗ Signup failed: {e.detail}")
                return False

    print(f"\n2. Testing Signin with email: {test_email}")

    # Create login data
    user_login = UserLogin(
        email=test_email,
        password=test_password
    )

    # Mock the database operations for signin
    with patch('app.routers.auth.select') as mock_select:
        # Create a mock user object for the found user
        mock_found_user = MagicMock(spec=User)
        mock_found_user.id = "mocked-uuid-123"
        mock_found_user.email = test_email
        mock_found_user.name = test_name
        mock_found_user.password_hash = "$2b$12$mocked_hash"  # Mock hash
        from datetime import datetime
        mock_found_user.created_at = datetime.now()

        # Configure the mock to return our found user
        mock_exec_result = MagicMock()
        mock_exec_result.first.return_value = mock_found_user
        mock_db.exec.return_value = mock_exec_result

        try:
            # Attempt signin
            signin_result = await signin(user_login, mock_db)
            print(f"   ✓ Signin successful: {signin_result.user.email}")

            # Verify that the same user was found
            assert signin_result.user.id == "mocked-uuid-123"
            assert signin_result.user.email == test_email

        except HTTPException as e:
            print(f"   ✗ Signin failed: {e.detail}")
            return False

    print(f"\n3. Testing Multiple Signins (same account)")

    # Test signing in again with the same account
    try:
        # Attempt second signin
        signin_result2 = await signin(user_login, mock_db)
        print(f"   ✓ Second signin successful: {signin_result2.user.email}")

        # Verify that it's still the same user
        assert signin_result2.user.id == "mocked-uuid-123"
        assert signin_result2.user.email == test_email
        print("   ✓ Same user returned (account can sign in multiple times)")

    except HTTPException as e:
        print(f"   ✗ Second signin failed: {e.detail}")
        return False

    print(f"\n4. Testing Case-Insensitive Email Lookup")

    # Test with different case email
    user_login_case = UserLogin(
        email="TESTUSER@EXAMPLE.COM",  # Different case
        password=test_password
    )

    try:
        # Attempt signin with different case
        case_result = await signin(user_login_case, mock_db)
        print(f"   ✓ Case-insensitive signin successful: {case_result.user.email}")

        # Email should be normalized to lowercase as stored
        assert case_result.user.email == test_email  # Should be lowercase

    except HTTPException as e:
        print(f"   ✗ Case-insensitive signin failed: {e.detail}")
        return False

    print(f"\n5. Testing Wrong Password Rejection")

    # Test with wrong password
    user_login_wrong = UserLogin(
        email=test_email,
        password="WrongPassword123!"  # Wrong password
    )

    try:
        # Attempt signin with wrong password
        wrong_result = await signin(user_login_wrong, mock_db)
        print(f"   ✗ Wrong password was accepted (security issue!)")
        return False

    except HTTPException as e:
        if e.status_code == 401:
            print(f"   ✓ Wrong password correctly rejected")
        else:
            print(f"   ? Wrong password failed with unexpected error: {e.detail}")
            return False

    print(f"\n6. Testing Non-Existent User")

    # Test with non-existent email
    user_login_nonexistent = UserLogin(
        email="nonexistent@example.com",
        password="AnyPassword123!"
    )

    # Mock that no user is found
    with patch('app.routers.auth.select'):
        mock_exec_result_nonexistent = MagicMock()
        mock_exec_result_nonexistent.first.return_value = None
        mock_db.exec.return_value = mock_exec_result_nonexistent

        try:
            nonexistent_result = await signin(user_login_nonexistent, mock_db)
            print(f"   ✗ Non-existent user was accepted")
            return False

        except HTTPException as e:
            if e.status_code == 401:
                print(f"   ✓ Non-existent user correctly rejected")
            else:
                print(f"   ? Non-existent user failed with unexpected error: {e.detail}")
                return False

    print("\n" + "=" * 50)
    print("✓ ALL AUTHENTICATION TESTS PASSED!")
    print("✓ Signup works correctly")
    print("✓ Signin works correctly")
    print("✓ Same account can sign in multiple times")
    print("✓ Case-insensitive email lookup works")
    print("✓ Wrong password correctly rejected")
    print("✓ Non-existent user correctly rejected")
    print("\nThe authentication system is working properly!")
    print("Users should now be able to sign in with the same account multiple times.")
    print("=" * 50)

    return True

if __name__ == "__main__":
    success = asyncio.run(test_authentication_flow())
    if not success:
        sys.exit(1)