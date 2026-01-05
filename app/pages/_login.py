"""
Login Page
"""

import streamlit as st
from auth.firebase_auth import SimpleAuth
from database.db import Database
from utils.ui_helpers import apply_custom_css, show_error, show_success

def show_login_page():
    """Display login page"""
    apply_custom_css()
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>✨ AI Content Creator</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Create amazing content with AI</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tab for Login and Sign Up
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        # Login Tab
        with tab1:
            st.markdown("### Welcome Back!")
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="Enter your email")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_login1, col_login2 = st.columns(2)
                with col_login1:
                    submit_login = st.form_submit_button("Login", use_container_width=True)
                with col_login2:
                    forgot_password = st.form_submit_button("Forgot Password?", use_container_width=True)
                
                if submit_login:
                    if email and password:
                        with st.spinner("Logging in..."):
                            auth = SimpleAuth()
                            result = auth.sign_in(email, password)
                            
                            if result["success"]:
                                # Store user info in session
                                st.session_state.user = result["user"]
                                st.session_state.user_id = result["user_id"]
                                st.session_state.email = result["email"]
                                
                                show_success("Login successful!")
                                st.rerun()
                            else:
                                show_error(result["error"])
                    else:
                        show_error("Please enter both email and password")
                
                if forgot_password:
                    show_error("Password reset feature: Please contact administrator or use 'Change Password' in profile after logging in.")
        
        # Sign Up Tab
        with tab2:
            st.markdown("### Create Account")
            with st.form("signup_form"):
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("Password", type="password", placeholder="At least 6 characters", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                display_name = st.text_input("Display Name (Optional)", placeholder="Your name")
                
                submit_signup = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit_signup:
                    if new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            show_error("Passwords do not match")
                        elif len(new_password) < 6:
                            show_error("Password should be at least 6 characters")
                        else:
                            with st.spinner("Creating account..."):
                                auth = SimpleAuth()
                                result = auth.sign_up(new_email, new_password, display_name)
                                
                                if result["success"]:
                                    # Store user info in session
                                    st.session_state.user = result["user"]
                                    st.session_state.user_id = result["user_id"]
                                    st.session_state.email = result["email"]
                                    
                                    show_success("Account created successfully!")
                                    st.rerun()
                                else:
                                    show_error(result["error"])
                    else:
                        show_error("Please fill in all required fields")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #999; font-size: 0.85rem;'>By continuing, you agree to our Terms of Service and Privacy Policy</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_login_page()
