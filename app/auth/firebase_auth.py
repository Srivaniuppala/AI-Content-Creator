"""
Simple Authentication Module
Handles user authentication with password hashing
"""

import hashlib
import secrets
import streamlit as st
from typing import Optional, Dict
from database.db import Database

class SimpleAuth:
    def __init__(self):
        """Initialize authentication"""
        self.db = Database()
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """
        Hash password with salt
        
        Args:
            password: Plain text password
            salt: Optional salt (generates new if not provided)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return pwd_hash.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            hashed_password: Stored hash
            salt: Stored salt
            
        Returns:
            True if password matches
        """
        pwd_hash, _ = SimpleAuth.hash_password(password, salt)
        return pwd_hash == hashed_password
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def sign_up(self, email: str, password: str, display_name: str = None) -> Dict:
        """
        Create a new user account
        
        Args:
            email: User email
            password: User password
            display_name: Optional display name
            
        Returns:
            Dictionary with user info or error
        """
        try:
            # Validate email format
            if not self.validate_email(email):
                return {"success": False, "error": "Invalid email format"}
            
            # Validate password length
            if len(password) < 6:
                return {"success": False, "error": "Password should be at least 6 characters"}
            
            # Check if email already exists
            existing_user = self.db.get_user_by_email(email)
            if existing_user:
                return {"success": False, "error": "Email already exists"}
            
            # Hash password
            pwd_hash, salt = self.hash_password(password)
            
            # Create user
            user_id = self.db.create_user_with_password(email, pwd_hash, salt, display_name)
            
            if user_id:
                user = self.db.get_user_by_id(user_id)
                return {
                    "success": True,
                    "user": user,
                    "user_id": user_id,
                    "email": email
                }
            else:
                return {"success": False, "error": "Failed to create user"}
                
        except Exception as e:
            return {"success": False, "error": f"Sign up failed: {str(e)}"}
    
    def sign_in(self, email: str, password: str) -> Dict:
        """
        Sign in existing user
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user info or error
        """
        try:
            # Get user by email
            user = self.db.get_user_by_email(email)
            
            if not user:
                return {"success": False, "error": "Invalid email or password"}
            
            # Verify password
            if not self.verify_password(password, user['password_hash'], user['salt']):
                return {"success": False, "error": "Invalid email or password"}
            
            return {
                "success": True,
                "user": user,
                "user_id": user['id'],
                "email": user['email']
            }
            
        except Exception as e:
            return {"success": False, "error": f"Sign in failed: {str(e)}"}
    
    def sign_out(self):
        """Sign out current user"""
        keys_to_remove = ['user', 'user_id', 'email', 'current_session_id']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently authenticated user from session"""
        if 'user' in st.session_state:
            return st.session_state.user
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return 'user' in st.session_state and st.session_state.user is not None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict:
        """
        Change user password
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            Success or error message
        """
        try:
            # Get user
            user = self.db.get_user_by_id(user_id)
            if not user:
                return {"success": False, "error": "User not found"}
            
            # Verify old password
            if not self.verify_password(old_password, user['password_hash'], user['salt']):
                return {"success": False, "error": "Current password is incorrect"}
            
            # Validate new password
            if len(new_password) < 6:
                return {"success": False, "error": "New password should be at least 6 characters"}
            
            # Hash new password
            pwd_hash, salt = self.hash_password(new_password)
            
            # Update password
            if self.db.update_user_password(user_id, pwd_hash, salt):
                return {"success": True, "message": "Password changed successfully"}
            else:
                return {"success": False, "error": "Failed to update password"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
