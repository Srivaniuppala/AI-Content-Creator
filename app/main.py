"""
Main Application Entry Point
AI Content Creator - Streamlit App
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules (renamed with _ to prevent Streamlit auto-discovery)
from pages._login import show_login_page
from pages._home import show_home_page
from pages._history import show_history_page
from pages._profile import show_profile_page
from auth.firebase_auth import SimpleAuth
from utils.ui_helpers import set_page_config, apply_custom_css

# Configure page - set to wide mode and custom title
st.set_page_config(
    page_title="AI Content Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

def show_navigation():
    """Display navigation sidebar"""
    with st.sidebar:
        st.markdown("# 🎨 AI Content Creator")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True, 
                    type="primary" if st.session_state.page == 'home' else "secondary"):
            st.session_state.page = 'home'
            if 'current_session_id' in st.session_state:
                del st.session_state.current_session_id
            st.rerun()
        
        if st.button("📜 History", use_container_width=True,
                    type="primary" if st.session_state.page == 'history' else "secondary"):
            st.session_state.page = 'history'
            st.rerun()
        
        if st.button("👤 Profile", use_container_width=True,
                    type="primary" if st.session_state.page == 'profile' else "secondary"):
            st.session_state.page = 'profile'
            st.rerun()
        
        st.markdown("---")
        
        # User info
        if 'email' in st.session_state:
            st.markdown(f"**Logged in as:**")
            st.caption(st.session_state.email)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            auth = SimpleAuth()
            auth.sign_out()
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 About")
        st.info("""
        AI Content Creator uses advanced language models to generate personalized content for your needs.
        
        **Features:**
        - Multiple content types
        - Chat history
        - Customizable tone & length
        - Save & organize content
        """)
        
        st.markdown("---")
        st.caption("© 2026 AI Content Creator")

def main():
    """Main application logic"""
    initialize_session_state()
    apply_custom_css()
    
    # Check authentication
    auth = SimpleAuth()
    
    if not auth.is_authenticated():
        # Show login page
        show_login_page()
    else:
        # Show main application
        show_navigation()
        
        # Route to appropriate page
        if st.session_state.page == 'home':
            show_home_page()
        elif st.session_state.page == 'history':
            show_history_page()
        elif st.session_state.page == 'profile':
            show_profile_page()
        else:
            show_home_page()

if __name__ == "__main__":
    main()
