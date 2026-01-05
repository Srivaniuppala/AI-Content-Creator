"""
History Page - View past generated content
"""

import streamlit as st
from database.db import Database
from utils.ui_helpers import apply_custom_css, show_header
from datetime import datetime

def show_history_page():
    """Display history page with generated content"""
    apply_custom_css()
    show_header("📜 Content History", "View and manage your generated content")
    
    db = Database()
    
    # Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Search in your content...")
    
    with col2:
        content_types = db.get_all_content_types()
        filter_type = st.selectbox(
            "Filter by Type",
            ["All"] + [ct['name'] for ct in content_types]
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            ["Recent First", "Oldest First", "Favorites"]
        )
    
    st.markdown("---")
    
    # Get generated content
    generated_content = db.get_user_generated_content(st.session_state.user_id, limit=100)
    
    # Apply filters
    if filter_type != "All":
        generated_content = [gc for gc in generated_content if gc['content_type_name'] == filter_type]
    
    if search_query:
        search_lower = search_query.lower()
        generated_content = [
            gc for gc in generated_content 
            if search_lower in gc['prompt'].lower() or search_lower in gc['generated_text'].lower()
        ]
    
    # Apply sorting
    if sort_by == "Oldest First":
        generated_content = sorted(generated_content, key=lambda x: x['created_at'])
    elif sort_by == "Favorites":
        generated_content = sorted(generated_content, key=lambda x: x['is_favorite'], reverse=True)
    
    # Display stats
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Total Content", len(db.get_user_generated_content(st.session_state.user_id, limit=1000)))
    
    with col_stat2:
        favorites_count = len([gc for gc in db.get_user_generated_content(st.session_state.user_id, limit=1000) if gc['is_favorite']])
        st.metric("Favorites", favorites_count)
    
    with col_stat3:
        if generated_content:
            latest = datetime.fromisoformat(str(generated_content[0]['created_at']))
            days_ago = (datetime.now() - latest).days
            st.metric("Last Created", f"{days_ago} days ago" if days_ago > 0 else "Today")
    
    with col_stat4:
        st.metric("Showing", len(generated_content))
    
    st.markdown("---")
    
    # Display content
    if generated_content:
        for idx, content in enumerate(generated_content):
            with st.container():
                col_main, col_actions = st.columns([5, 1])
                
                with col_main:
                    # Content header
                    st.markdown(f"""
                        <div class="history-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <span class="content-badge">{content['content_type_name']}</span>
                                <span class="timestamp">{datetime.fromisoformat(str(content['created_at'])).strftime('%b %d, %Y %I:%M %p')}</span>
                            </div>
                            <h4 style="margin: 0.5rem 0;">{'⭐ ' if content['is_favorite'] else ''}{content['prompt'][:100]}{'...' if len(content['prompt']) > 100 else ''}</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Expandable content
                    with st.expander("View Content"):
                        st.markdown(f"**Prompt:**")
                        st.info(content['prompt'])
                        
                        st.markdown(f"**Generated Content:**")
                        st.success(content['generated_text'])
                        
                        # Metadata
                        col_meta1, col_meta2, col_meta3 = st.columns(3)
                        with col_meta1:
                            st.caption(f"**Tone:** {content['tone'] or 'N/A'}")
                        with col_meta2:
                            st.caption(f"**Length:** {content['length_preference'] or 'N/A'}")
                        with col_meta3:
                            st.caption(f"**Words:** {len(content['generated_text'].split())}")
                
                with col_actions:
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Favorite button
                    if st.button("⭐" if not content['is_favorite'] else "★", 
                               key=f"fav_{content['id']}", 
                               help="Toggle favorite",
                               use_container_width=True):
                        db.toggle_favorite(content['id'])
                        st.rerun()
                    
                    # Copy button
                    st.download_button(
                        "📋",
                        content['generated_text'],
                        file_name=f"content_{content['id']}.txt",
                        key=f"copy_{content['id']}",
                        help="Download content",
                        use_container_width=True
                    )
                    
                    # Continue chat button
                    if content['session_id']:
                        if st.button("💬", 
                                   key=f"continue_{content['id']}", 
                                   help="Continue this chat",
                                   use_container_width=True):
                            st.session_state.current_session_id = content['session_id']
                            st.session_state.page = 'home'
                            st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("📭 No content found. Start creating some amazing content!")
        if st.button("➕ Create Content", type="primary"):
            st.session_state.page = 'home'
            st.rerun()
    
    # Pagination info
    if len(generated_content) >= 100:
        st.info("💡 Showing recent 100 items. Use filters to narrow down results.")

if __name__ == "__main__":
    show_history_page()
