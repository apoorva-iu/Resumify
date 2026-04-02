import streamlit as st
from groq import Groq
# NOTE: We only need get_user_sessions (renamed from get_user_chats) 
# and the new specific functions for session management.
from utils.database import create_new_session, save_message, get_user_sessions, get_chat_messages_by_id
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# --- Setup Functions ---

def load_previous_sessions(user_id):
    """
    Loads chat session metadata (ID, Title, Date) from the database.
    """
    try:
        # get_user_sessions returns list of (session_id, title, created_at)
        sessions = get_user_sessions(user_id) 
        
        # Convert list of tuples to a dictionary for easy lookup by ID
        session_dict = {}
        for session_id, title, created_at in sessions:
            # Storing key metadata needed for the expander link
            session_dict[session_id] = {
                "title": title,
                "created_at": created_at
            }
            
        return session_dict

    except Exception as e:
        # This catches errors if the DB file/table is missing
        st.error(f"Error connecting to database to load sessions: {e}")
        return {}

# Function to clear current chat state and start fresh
def clear_current_chat():
    st.session_state.selected_chat_id = None
    st.session_state.chat_messages = [] 
    st.session_state.current_session_db_id = None
    st.rerun()

def main():

    # Require login
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please login first to access the chatbot.")
        st.stop()

    load_dotenv()

    # --- Styling (Timestamps removed) ---
    st.markdown("""
    <style>
    /* Timestamps removed from CSS definitions for cleaner look */
    .user-message {
        background: linear-gradient(135deg, #03055B 0%, #4C516D 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: 16px;
        line-height: 1.5;
    }
    .bot-message {
         background: linear-gradient(135deg, #03055B 0%, #4C516D 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        font-size: 16px;
        line-height: 1.5;
    }
    .clear-both {
        clear: both;
    }
    /* Ensure the main chat container has room for downward flow */
    .st-emotion-cache-1c7y2qn {
        display: flex;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Session Initialization ---
    user_id = st.session_state.user_id
    username = st.session_state.username

    st.title("🤖 AI Chatbot Assistant")
    st.markdown(f"### Welcome, **{username}**!")
    st.divider()

    # Groq client
    client = None
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    except Exception:
        st.warning("⚠️ GROQ_API_KEY missing — AI disabled.")
    
    # 1. Current Session Messages (list of dictionaries)
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # 2. Previous Chat Sessions (dictionary of {session_id: {title, created_at}})
    if "previous_chat_sessions" not in st.session_state:
        st.session_state.previous_chat_sessions = load_previous_sessions(user_id)
        
    # 3. Selected Historical Chat ID (int or None) - used only for triggering the load logic
    if "selected_chat_id" not in st.session_state:
        st.session_state.selected_chat_id = None 

    # 4. ID of the current working session (int or None) - holds the ID of the chat currently being continued
    if "current_session_db_id" not in st.session_state:
        st.session_state.current_session_db_id = None
        
    # --- Logic for loading and continuing an old chat ---
    if st.session_state.selected_chat_id is not None:
        session_id_to_load = st.session_state.selected_chat_id
        
        try:
            # 1. Fetch messages from DB
            historical_chat_messages = get_chat_messages_by_id(session_id_to_load) # (sender, message, timestamp)
            
            # 2. Convert DB format to current session state format
            loaded_messages = []
            
            # Since the DB stores messages individually but the state stores pairs:
            user_msg = None
            user_ts = None
            
            for sender, message, timestamp in historical_chat_messages:
                if sender == 'user':
                    user_msg = message
                    user_ts = timestamp
                elif sender == 'bot' and user_msg is not None:
                    loaded_messages.append({
                        "user_message": user_msg,
                        "user_timestamp": user_ts,
                        "bot_message": message,
                        "bot_timestamp": timestamp
                    })
                    user_msg = None # Reset for next pair
            
            # 3. Update session state to continue the chat
            st.session_state.chat_messages = loaded_messages
            st.session_state.current_session_db_id = session_id_to_load
            
            # 4. Reset selected_chat_id so the UI switches to the "Current Conversation" logic below
            st.session_state.selected_chat_id = None 
            st.rerun()
            
        except Exception as e:
            st.error(f"Error loading chat history: {e}")
            st.session_state.selected_chat_id = None # Stop trying to load
            st.rerun()

    # --- PREVIOUS CHAT HISTORY (Expander) ---
    with st.expander("📜 View Previous Chat History", expanded=False):

        if not st.session_state.previous_chat_sessions:
            st.info("No previous chat sessions found.")
        else:
            # Display chat sessions as buttons/links
            for session_id, metadata in st.session_state.previous_chat_sessions.items():
                title = metadata['title']
                timestamp = metadata['created_at']
                
                # Button text only shows title and creation timestamp (no ID)
                # I'm adding the timestamp back here as it gives context on when the chat was started
                if st.button(f"**{title}**", key=f"session_{session_id}"): 
                    st.session_state.selected_chat_id = session_id
                    st.rerun()

    st.divider()

    # ------------------------- CURRENT CHAT (NEW/CONTINUED CHAT) -------------------------
    st.markdown("### New Chat")
    
    # Display status: only show a status if CONTINUING a saved chat
    is_continuing_chat = False
    if st.session_state.current_session_db_id is not None:
        session_meta = st.session_state.previous_chat_sessions.get(st.session_state.current_session_db_id)
        if session_meta:
            st.markdown("")
            is_continuing_chat = True
        
    # ONLY add the horizontal line if we are CONTINUING a chat (i.e., we just displayed a status line).
    # If it's a new chat, we skip this to avoid the empty line below "Current Conversation".
    if is_continuing_chat:
         st.markdown("---")

    # Show current chat messages (in correct order: oldest first, newest last)
    for chat in st.session_state.chat_messages:
        
        # USER FIRST - Timestamps removed
        st.markdown(f"""
        <div class="user-message">
            <strong>🧑‍💻 You:</strong><br>
            {chat['user_message']}
        </div>
        <div class="clear-both"></div>
        """, unsafe_allow_html=True)

        # BOT SECOND - Timestamps removed
        st.markdown(f"""
        <div class="bot-message">
            <strong>🤖 AI Assistant:</strong><br>
            {chat['bot_message']}
        </div>
        <div class="clear-both"></div>
        """, unsafe_allow_html=True)

    st.divider()

    # ------------------------- INPUT BOX (Always visible for continuation) -------------------------
    with st.container():
        with st.form("chat_form", clear_on_submit=True):

            cols = st.columns([5, 1])

            with cols[0]:
                user_input = st.text_input("Message", placeholder="Type your message…", label_visibility="collapsed")

            with cols[1]:
                submitted = st.form_submit_button("Send")

    # ------------------------- SEND MESSAGE -------------------------
    if submitted and user_input.strip():

        ts_user = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- DB SESSION MANAGEMENT: Create session on first message of a NEW chat ---
        if st.session_state.current_session_db_id is None:
            # Create a simple title based on the first few words of the message
            title = user_input.strip()[:30] + ('...' if len(user_input.strip()) > 30 else '')
            try:
                session_id = create_new_session(user_id, title)
                st.session_state.current_session_db_id = session_id
                # Update the previous chats list immediately to show the new chat in the expander
                st.session_state.previous_chat_sessions = load_previous_sessions(user_id) 
            except Exception as e:
                st.error(f"Error creating new chat session: {e}")
                st.stop()
        
        current_session_id = st.session_state.current_session_db_id
        
        # Generate AI reply
        bot_reply = "AI disabled — missing API key."
        if client:
            try:
                # Construct conversation history for context
                history = [{"role": "system", "content": "You are a helpful AI assistant."}]
                
                # Include past messages for context
                for c in st.session_state.chat_messages[-5:]:
                    history.append({"role": "user", "content": c["user_message"]})
                    history.append({"role": "assistant", "content": c["bot_message"]})
                    
                history.append({"role": "user", "content": user_input.strip()})
                
                reply = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=history
                )
                bot_reply = reply.choices[0].message.content
            except Exception as e:
                bot_reply = f"Error: {e}"
        
        ts_bot = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Store in CURRENT chat state
        st.session_state.chat_messages.append({
            "user_message": user_input.strip(),
            "user_timestamp": ts_user,
            "bot_message": bot_reply,
            "bot_timestamp": ts_bot
        })
        
        # --- DB MESSAGE SAVING ---
        try:
            # Save User message
            save_message(current_session_id, 'user', user_input.strip())
            # Save Bot message
            save_message(current_session_id, 'bot', bot_reply)
        except Exception as e:
            st.error(f"Error saving messages to DB: {e}")

        st.rerun()

    # ------------------------- CLEAR CHAT -------------------------
    st.divider()
    if st.button("Clear & Start New Chat", type="secondary"):

        # Reload session metadata (just in case)
        st.session_state.previous_chat_sessions = load_previous_sessions(user_id)

        # Clear current chat state and session ID
        clear_current_chat()


if __name__ == "__main__":
    # Ensure all necessary session states are initialized for non-login pages
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = None
        st.session_state['username'] = None
        
    main()

