"""
Profile Page - User profile and settings
"""

import streamlit as st
from database.db import Database
from auth.firebase_auth import SimpleAuth
from utils.ui_helpers import apply_custom_css, show_success, show_error
from datetime import datetime

def show_profile_page():
    """Display profile page"""
    apply_custom_css()
    
    db = Database()
    user = db.get_user_by_id(st.session_state.user_id)
    
    if not user:
        show_error("User not found")
        return
    
    # Profile Header
    st.markdown(f"""
        <div class="profile-header">
            <div style="font-size: 4rem;">👤</div>
            <h2 style="margin: 0.5rem 0;">{user['display_name'] or 'User'}</h2>
            <p style="margin: 0;">{user['email']}</p>
            <p style="margin: 0.5rem 0; opacity: 0.8;">Member since {datetime.fromisoformat(str(user['created_at'])).strftime('%B %Y')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Profile Info", "⚙️ Preferences", "📊 Statistics"])
    
    # Profile Info Tab
    with tab1:
        st.markdown("### Edit Profile")
        
        with st.form("profile_form"):
            display_name = st.text_input(
                "Display Name",
                value=user['display_name'] or '',
                placeholder="Enter your name"
            )
            
            # Email is read-only
            st.text_input(
                "Email",
                value=user['email'],
                disabled=True,
                help="Email cannot be changed"
            )
            
            profile_picture_url = st.text_input(
                "Profile Picture URL (Optional)",
                value=user['profile_picture_url'] or '',
                placeholder="https://example.com/image.jpg"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit_profile = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")
            
            if submit_profile:
                if db.update_user_profile(st.session_state.user_id, display_name, profile_picture_url):
                    show_success("Profile updated successfully!")
                    st.rerun()
                else:
                    show_error("Failed to update profile")
        
        st.markdown("---")
        st.markdown("### 🔑 Change Password")
        
        with st.form("password_form"):
            old_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_new_password = st.text_input("Confirm New Password", type="password")
            
            submit_password = st.form_submit_button("🔑 Change Password", use_container_width=True, type="primary")
            
            if submit_password:
                if not old_password or not new_password or not confirm_new_password:
                    show_error("Please fill in all password fields")
                elif new_password != confirm_new_password:
                    show_error("New passwords do not match")
                else:
                    auth = SimpleAuth()
                    result = auth.change_password(st.session_state.user_id, old_password, new_password)
                    if result['success']:
                        show_success(result['message'])
                    else:
                        show_error(result['error'])
    
    # Preferences Tab
    with tab2:
        st.markdown("### Content Preferences")
        
        # Get current preferences
        prefs = db.get_user_preferences(st.session_state.user_id)
        
        with st.form("preferences_form"):
            default_tone = st.selectbox(
                "Default Tone",
                ["professional", "casual", "creative", "persuasive", "informative"],
                index=["professional", "casual", "creative", "persuasive", "informative"].index(
                    prefs['default_tone'] if prefs else 'professional'
                )
            )
            
            default_length = st.selectbox(
                "Default Length",
                ["short", "medium", "long"],
                index=["short", "medium", "long"].index(
                    prefs['default_length'] if prefs else 'medium'
                )
            )
            
            theme = st.selectbox(
                "Theme",
                ["light", "dark"],
                index=["light", "dark"].index(
                    prefs['theme'] if prefs else 'light'
                ),
                help="Theme preference (currently visual only)"
            )
            
            submit_prefs = st.form_submit_button("💾 Save Preferences", use_container_width=True, type="primary")
            
            if submit_prefs:
                if db.create_or_update_preferences(
                    st.session_state.user_id,
                    default_tone,
                    default_length,
                    theme
                ):
                    show_success("Preferences saved successfully!")
                    st.rerun()
                else:
                    show_error("Failed to save preferences")
        
        st.markdown("---")
        st.markdown("### Account Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚪 Logout", use_container_width=True, type="secondary", key="profile_logout_btn"):
                auth = SimpleAuth()
                auth.sign_out()
                st.session_state.clear()
                st.rerun()
        
        with col2:
            if st.button("🗑️ Delete Account", use_container_width=True, type="secondary", key="delete_account_btn"):
                st.warning("⚠️ Account deletion is not yet implemented. Contact support.")
    
    # Statistics Tab
    with tab3:
        st.markdown("### Your Statistics")
        
        # Get statistics
        generated_content = db.get_user_generated_content(st.session_state.user_id, limit=1000)
        sessions = db.get_user_chat_sessions(st.session_state.user_id, limit=1000)
        content_types = db.get_all_content_types()
        
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Content", len(generated_content))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Chat Sessions", len(sessions))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            favorites = len([gc for gc in generated_content if gc['is_favorite']])
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Favorites", favorites)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            total_words = sum(len(gc['generated_text'].split()) for gc in generated_content)
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Words", f"{total_words:,}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Content type breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Content by Type")
            
            type_counts = {}
            for gc in generated_content:
                ct_name = gc['content_type_name']
                type_counts[ct_name] = type_counts.get(ct_name, 0) + 1
            
            if type_counts:
                for ct_name, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                    st.progress(count / len(generated_content), text=f"{ct_name}: {count}")
            else:
                st.info("No content generated yet")
        
        with col2:
            st.markdown("### 📈 Recent Activity")
            
            if generated_content:
                # Group by date
                from collections import defaultdict
                date_counts = defaultdict(int)
                
                for gc in generated_content[:30]:  # Last 30 items
                    date = datetime.fromisoformat(str(gc['created_at'])).strftime('%Y-%m-%d')
                    date_counts[date] += 1
                
                # Display recent dates
                for date, count in sorted(date_counts.items(), reverse=True)[:7]:
                    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%b %d')
                    st.write(f"**{formatted_date}**: {count} content created")
            else:
                st.info("No activity yet")
        
        st.markdown("---")
        
        # Most used settings
        st.markdown("### 🎯 Your Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Most Used Tone:**")
            tones = [gc['tone'] for gc in generated_content if gc['tone']]
            if tones:
                most_common_tone = max(set(tones), key=tones.count)
                st.info(f"📝 {most_common_tone.title()}")
            else:
                st.info("No data yet")
        
        with col2:
            st.markdown("**Most Used Length:**")
            lengths = [gc['length_preference'] for gc in generated_content if gc['length_preference']]
            if lengths:
                most_common_length = max(set(lengths), key=lengths.count)
                st.info(f"📏 {most_common_length.title()}")
            else:
                st.info("No data yet")

if __name__ == "__main__":
    show_profile_page()
