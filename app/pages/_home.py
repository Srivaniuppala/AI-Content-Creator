"""
Home Page - Content Generation Interface
"""

import streamlit as st
from database.db import Database
from services.ollama_service import OllamaService
from utils.ui_helpers import apply_custom_css, show_header, show_error, show_success
from datetime import datetime

def show_home_page():
    """Display home page with content generation"""
    apply_custom_css()
    show_header("🎨 Create Content", "Generate amazing content with AI")
    
    db = Database()
    ollama = OllamaService()
    
    # Check Groq API connection
    if not ollama.check_connection():
        st.error("⚠️ Unable to connect to Groq API. Please check your API key configuration.")
        return
    
    # Sidebar for settings
    with st.sidebar:
        st.markdown("### ⚙️ Content Settings")
        
        # Get content types
        content_types = db.get_all_content_types()
        content_type_names = [ct['name'] for ct in content_types]
        
        selected_content_type = st.selectbox(
            "Content Type",
            content_type_names,
            help="Select the type of content you want to generate"
        )
        
        tone = st.selectbox(
            "Tone",
            ["Professional", "Casual", "Creative", "Persuasive", "Informative"],
            help="Choose the tone for your content"
        )
        
        length = st.selectbox(
            "Length",
            ["Short", "Medium", "Long"],
            help="Select the desired length"
        )
        
        st.markdown("---")
        
        # Chat sessions
        st.markdown("### 💬 Recent Chats")
        user_sessions = db.get_user_chat_sessions(st.session_state.user_id, limit=10)
        
        if user_sessions:
            for session in user_sessions:
                if st.button(f"📝 {session['title'][:30]}...", key=f"session_{session['id']}", use_container_width=True):
                    st.session_state.current_session_id = session['id']
                    st.rerun()
        else:
            st.info("No chat history yet")
        
        if st.button("➕ New Chat", use_container_width=True):
            if 'current_session_id' in st.session_state:
                del st.session_state.current_session_id
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Check if continuing a chat or starting new
        if 'current_session_id' in st.session_state:
            session = db.get_chat_session(st.session_state.current_session_id)
            if session:
                st.info(f"📝 Continuing: {session['title']}")
                
                # Display chat history
                messages = db.get_chat_messages(st.session_state.current_session_id)
                
                st.markdown("### Chat History")
                for msg in messages:
                    if msg['role'] == 'user':
                        st.markdown(f'<div class="user-message"><b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="assistant-message"><b>AI:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
        
        # Input area
        st.markdown("### 💭 What would you like to create?")
        
        user_prompt = st.text_area(
            "Enter your prompt",
            placeholder="Example: Write a LinkedIn post about the importance of AI in modern business...",
            height=150,
            key="user_prompt"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
        
        with col_btn1:
            generate_btn = st.button("✨ Generate Content", use_container_width=True, type="primary")
        
        with col_btn2:
            if 'current_session_id' in st.session_state:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    del st.session_state.current_session_id
                    st.rerun()
        
        if generate_btn and user_prompt:
            with st.spinner("🎨 Generating content..."):
                try:
                    # Get content type ID
                    content_type_id = next(
                        (ct['id'] for ct in content_types if ct['name'] == selected_content_type),
                        None
                    )
                    
                    # Create or get session
                    if 'current_session_id' not in st.session_state:
                        # Create new session
                        title = user_prompt[:50] + "..." if len(user_prompt) > 50 else user_prompt
                        session_id = db.create_chat_session(
                            st.session_state.user_id,
                            title,
                            content_type_id
                        )
                        st.session_state.current_session_id = session_id
                    else:
                        session_id = st.session_state.current_session_id
                    
                    # Save user message
                    db.add_chat_message(session_id, 'user', user_prompt)
                    
                    # Create optimized prompt
                    system_prompt = ollama.create_content_prompt(
                        selected_content_type,
                        user_prompt,
                        tone.lower(),
                        length.lower()
                    )
                    
                    # Generate content with streaming
                    st.markdown("### ✨ Generated Content")
                    generated_text = ""
                    placeholder = st.empty()
                    
                    for chunk in ollama.generate_content_stream(system_prompt):
                        generated_text += chunk
                        placeholder.markdown(f'<div class="assistant-message">{generated_text}</div>', unsafe_allow_html=True)
                    
                    # Save assistant message
                    db.add_chat_message(session_id, 'assistant', generated_text)
                    
                    # Save generated content
                    db.save_generated_content(
                        st.session_state.user_id,
                        session_id,
                        content_type_id,
                        user_prompt,
                        generated_text,
                        tone.lower(),
                        length.lower()
                    )
                    
                    show_success("Content generated successfully!")
                    
                    # Copy button
                    st.download_button(
                        "📋 Copy to Clipboard",
                        generated_text,
                        file_name=f"{selected_content_type.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    show_error(f"Error generating content: {str(e)}")
        
        elif generate_btn:
            show_error("Please enter a prompt")
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        # Get user stats
        generated_content = db.get_user_generated_content(st.session_state.user_id, limit=100)
        sessions = db.get_user_chat_sessions(st.session_state.user_id, limit=100)
        
        st.metric("Total Content", len(generated_content))
        st.metric("Chat Sessions", len(sessions))
        
        st.markdown("---")
        
        st.markdown("### 💡 Tips")
        st.info("""
        **Get better results:**
        - Be specific in your prompts
        - Mention target audience
        - Include key points to cover
        - Specify desired format
        """)
        
        st.markdown("### 🎯 Example Prompts")
        examples = [
            "Write about AI trends in 2026",
            "Create an email for product launch",
            "Draft a LinkedIn post about teamwork",
            "Generate ad copy for eco-friendly products"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example[:20]}", use_container_width=True):
                st.session_state.user_prompt = example
                st.rerun()

if __name__ == "__main__":
    show_home_page()
