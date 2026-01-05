"""
Streamlit UI Styling and Configuration
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Card styling */
        .card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 2px solid #e0e0e0;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76,175,80,0.2);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 2rem;
        }
        
        /* Success message */
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 1rem;
            color: #155724;
            margin: 1rem 0;
        }
        
        /* Error message */
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 1rem;
            color: #721c24;
            margin: 1rem 0;
        }
        
        /* Chat message styling */
        .user-message {
            background-color: #e3f2fd;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #2196F3;
        }
        
        .assistant-message {
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #4CAF50;
        }
        
        /* History card */
        .history-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
            border-left: 4px solid #2196F3;
            transition: all 0.3s ease;
        }
        
        .history-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateX(5px);
        }
        
        /* Profile section */
        .profile-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        
        /* Metric styling */
        .metric-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        /* Content type badge */
        .content-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            background-color: #e3f2fd;
            color: #1976d2;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        /* Timestamp styling */
        .timestamp {
            color: #757575;
            font-size: 0.85rem;
        }
        
        /* Loading animation */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .loading {
            animation: pulse 1.5s ease-in-out infinite;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
    """, unsafe_allow_html=True)

def set_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="AI Content Creator",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def show_header(title: str, subtitle: str = None):
    """Display page header"""
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")
    st.markdown("---")

def show_success(message: str):
    """Display success message"""
    st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)

def show_error(message: str):
    """Display error message"""
    st.markdown(f'<div class="error-box">❌ {message}</div>', unsafe_allow_html=True)

def show_info(message: str):
    """Display info message"""
    st.info(f"ℹ️ {message}")

def create_card(content: str):
    """Create a styled card"""
    st.markdown(f'<div class="card">{content}</div>', unsafe_allow_html=True)
