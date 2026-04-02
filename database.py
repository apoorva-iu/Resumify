import mysql.connector
import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'Qwert@123'),
    'database': os.getenv('MYSQL_DATABASE', 'resume'),
    'auth_plugin': 'mysql_native_password'
}
# ---

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Initialize database and tables
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Users table (Existing)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)

        # 2. Chat Sessions table (NEW)
        # Stores metadata for each separate conversation/chat "file"
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # 3. Messages table (Replaced user_chats)
        # Stores individual messages linked to a specific session
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id INT NOT NULL,
            sender VARCHAR(50) NOT NULL,
            message LONGTEXT,
            timestamp DATETIME,
            FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

# --- User Management (No Changes Needed) ---

# Password hashing
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Add new user
def add_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hash_password(password))
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return False
        raise
    finally:
        cursor.close()
        conn.close()

# Verify login credentials
def verify_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email FROM users WHERE email = %s AND password = %s",
        (email, hash_password(password))
    )
    user = cursor.fetchone() 
    cursor.close()
    conn.close()
    return user

# --- Chat Management (SIGNIFICANT CHANGES) ---

def create_new_session(user_id, title):
    """Creates a new chat session and returns its session_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()
    
    cursor.execute(
        "INSERT INTO chat_sessions (user_id, title, created_at) VALUES (%s, %s, %s)",
        (user_id, title, timestamp)
    )
    session_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return session_id

def save_message(session_id, sender, message):
    """Saves a single message linked to a specific session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()
    
    cursor.execute(
        "INSERT INTO messages (session_id, sender, message, timestamp) VALUES (%s, %s, %s, %s)",
        (session_id, sender, message, timestamp)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
# Function to get all chat sessions for the sidebar (Replaces get_user_chats)
def get_user_sessions(user_id):
    """Retrieves all chat sessions for the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT session_id, title, created_at FROM chat_sessions WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,)
    )
    sessions = cursor.fetchall()
    cursor.close()
    conn.close()
    return sessions

# Function to get messages for a selected chat (Implements get_chat_messages_by_id)
def get_chat_messages_by_id(session_id):
    """Retrieves all messages for a specific session_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message, timestamp FROM messages WHERE session_id = %s ORDER BY timestamp ASC",
        (session_id,)
    )
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return messages

# --- Compatibility Functions (for existing chat.py structure) ---

# We'll use this for saving the *first* message in the chat.py logic
# and then use save_message for subsequent messages.
def save_chat(user_id, session_id, sender, message):
    """
    A unified save function used by the app to handle both session creation (optional)
    and message saving.
    """
    save_message(session_id, sender, message)
    # The session_id must be managed in the Streamlit app state now.
    
def get_user_chats(user_id):
    """
    This function is replaced by get_user_sessions for the sidebar.
    Keeping it as a placeholder to avoid an initial import error, but it should 
    be removed/replaced in the main app's code.
    """
    return get_user_sessions(user_id)

if __name__ == "__main__":
    init_db()
    print("Database initialized with users, chat_sessions, and messages tables.")