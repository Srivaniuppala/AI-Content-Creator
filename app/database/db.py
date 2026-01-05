"""
Database connection and management
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self):
        """Initialize database connection parameters"""
        self.connection_string = os.getenv(
            "DATABASE_URL",
            "postgresql://content_admin:content_pass_2026@postgres:5432/content_creator"
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = psycopg2.connect(self.connection_string)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """
        Execute a SELECT query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of dictionaries with query results
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def execute_insert(self, query: str, params: tuple = None) -> Optional[int]:
        """
        Execute an INSERT query and return the inserted ID
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            ID of inserted row
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.rowcount > 0:
                    cursor.execute("SELECT lastval()")
                    return cursor.fetchone()[0]
                return None
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        Execute an UPDATE or DELETE query
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.rowcount
    
    # User operations
    def create_user_with_password(self, email: str, password_hash: str, salt: str, display_name: str = None) -> Optional[int]:
        """Create a new user with password"""
        query = """
            INSERT INTO users (email, password_hash, salt, display_name)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (email, password_hash, salt, display_name))
        return result[0]['id'] if result else None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = self.execute_query(query, (email,))
        return dict(result[0]) if result else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = self.execute_query(query, (user_id,))
        return dict(result[0]) if result else None
    
    def update_user_profile(self, user_id: int, display_name: str = None, 
                           profile_picture_url: str = None) -> bool:
        """Update user profile"""
        query = """
            UPDATE users 
            SET display_name = COALESCE(%s, display_name),
                profile_picture_url = COALESCE(%s, profile_picture_url)
            WHERE id = %s
        """
        return self.execute_update(query, (display_name, profile_picture_url, user_id)) > 0
    
    def update_user_password(self, user_id: int, password_hash: str, salt: str) -> bool:
        """Update user password"""
        query = """
            UPDATE users 
            SET password_hash = %s, salt = %s
            WHERE id = %s
        """
        return self.execute_update(query, (password_hash, salt, user_id)) > 0
    
    # Content type operations
    def get_all_content_types(self) -> List[Dict]:
        """Get all available content types"""
        query = "SELECT * FROM content_types ORDER BY name"
        result = self.execute_query(query)
        return [dict(row) for row in result] if result else []
    
    # Chat session operations
    def create_chat_session(self, user_id: int, title: str, content_type_id: int) -> Optional[int]:
        """Create a new chat session"""
        query = """
            INSERT INTO chat_sessions (user_id, title, content_type_id)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (user_id, title, content_type_id))
        return result[0]['id'] if result else None
    
    def get_user_chat_sessions(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get all chat sessions for a user"""
        query = """
            SELECT cs.*, ct.name as content_type_name
            FROM chat_sessions cs
            LEFT JOIN content_types ct ON cs.content_type_id = ct.id
            WHERE cs.user_id = %s
            ORDER BY cs.updated_at DESC
            LIMIT %s
        """
        result = self.execute_query(query, (user_id, limit))
        return [dict(row) for row in result] if result else []
    
    def get_chat_session(self, session_id: int) -> Optional[Dict]:
        """Get a specific chat session"""
        query = """
            SELECT cs.*, ct.name as content_type_name
            FROM chat_sessions cs
            LEFT JOIN content_types ct ON cs.content_type_id = ct.id
            WHERE cs.id = %s
        """
        result = self.execute_query(query, (session_id,))
        return dict(result[0]) if result else None
    
    def update_chat_session_title(self, session_id: int, title: str) -> bool:
        """Update chat session title"""
        query = "UPDATE chat_sessions SET title = %s WHERE id = %s"
        return self.execute_update(query, (title, session_id)) > 0
    
    # Chat message operations
    def add_chat_message(self, session_id: int, role: str, content: str) -> Optional[int]:
        """Add a message to a chat session"""
        query = """
            INSERT INTO chat_messages (session_id, role, content)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (session_id, role, content))
        return result[0]['id'] if result else None
    
    def get_chat_messages(self, session_id: int) -> List[Dict]:
        """Get all messages in a chat session"""
        query = """
            SELECT * FROM chat_messages
            WHERE session_id = %s
            ORDER BY created_at ASC
        """
        result = self.execute_query(query, (session_id,))
        return [dict(row) for row in result] if result else []
    
    # Generated content operations
    def save_generated_content(self, user_id: int, session_id: int, content_type_id: int,
                               prompt: str, generated_text: str, tone: str = None,
                               length_preference: str = None) -> Optional[int]:
        """Save generated content"""
        query = """
            INSERT INTO generated_content 
            (user_id, session_id, content_type_id, prompt, generated_text, tone, length_preference)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        result = self.execute_query(query, (user_id, session_id, content_type_id, 
                                           prompt, generated_text, tone, length_preference))
        return result[0]['id'] if result else None
    
    def get_user_generated_content(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get all generated content for a user"""
        query = """
            SELECT gc.*, ct.name as content_type_name
            FROM generated_content gc
            LEFT JOIN content_types ct ON gc.content_type_id = ct.id
            WHERE gc.user_id = %s
            ORDER BY gc.created_at DESC
            LIMIT %s
        """
        result = self.execute_query(query, (user_id, limit))
        return [dict(row) for row in result] if result else []
    
    def toggle_favorite(self, content_id: int) -> bool:
        """Toggle favorite status of generated content"""
        query = """
            UPDATE generated_content 
            SET is_favorite = NOT is_favorite
            WHERE id = %s
        """
        return self.execute_update(query, (content_id,)) > 0
    
    # User preferences operations
    def get_user_preferences(self, user_id: int) -> Optional[Dict]:
        """Get user preferences"""
        query = "SELECT * FROM user_preferences WHERE user_id = %s"
        result = self.execute_query(query, (user_id,))
        return dict(result[0]) if result else None
    
    def create_or_update_preferences(self, user_id: int, default_tone: str = None,
                                    default_length: str = None, theme: str = None) -> bool:
        """Create or update user preferences"""
        query = """
            INSERT INTO user_preferences (user_id, default_tone, default_length, theme)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                default_tone = COALESCE(EXCLUDED.default_tone, user_preferences.default_tone),
                default_length = COALESCE(EXCLUDED.default_length, user_preferences.default_length),
                theme = COALESCE(EXCLUDED.theme, user_preferences.theme),
                updated_at = CURRENT_TIMESTAMP
        """
        return self.execute_update(query, (user_id, default_tone, default_length, theme)) > 0
