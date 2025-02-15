import streamlit as st
import json
from datetime import datetime
from helpers import sleauth

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

def load_chat():
    """Load chat history from JSON file"""
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_chat(chat_data):
    """Save chat history to JSON file"""
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chat_data, f, indent=2)



# Load existing chat history
chat_history = load_chat()

# Display chat interface
st.title("Simple Chat App")

# Display chat history
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if user_input := st.chat_input("Type your question..."):
    # Add user message to chat
    user_message = {"role": "user", "content": user_input}
    chat_history.append(user_message)
    
    # Generate response
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response from sleauth
    response = sleauth(user_input)
    
    # Add assistant response to chat
    assistant_message = {"role": "assistant", "content": response}
    chat_history.append(assistant_message)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Save updated chat history
    save_chat(chat_history)