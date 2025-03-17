import streamlit as st
import os
from hiring_assistant import HiringAssistant
import time

# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👨‍💼",
    layout="centered"
)

# Define CSS for chat interface
st.markdown("""
<style>
.user-message {
    background-color: #e6f7ff;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    margin: 10px 0;
    max-width: 80%;
    align-self: flex-end;
    float: right;
    clear: both;
}
.assistant-message {
    background-color: #f0f2f5;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    margin: 10px 0;
    max-width: 80%;
    align-self: flex-start;
    float: left;
    clear: both;
}
.chat-container {
    height: 400px;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}
.message-container {
    overflow: hidden;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.messages = []
    st.session_state.assistant = None

def initialize_assistant():
    """Initialize the hiring assistant with API key."""
    api_key = st.session_state.api_key
    st.session_state.assistant = HiringAssistant(api_key=api_key)
    st.session_state.initialized = True
    
    # Generate initial greeting
    initial_response = st.session_state.assistant.process_user_input("Hello")
    st.session_state.messages.append({"role": "assistant", "content": initial_response})

# Main application
st.title("TalentScout Hiring Assistant")

# API key input (in sidebar for cleanliness)
with st.sidebar:
    st.header("Configuration")
    if not st.session_state.initialized:
        api_key = st.text_input("Enter your OpenAI API Key", type="password")
        st.session_state.api_key = api_key
        if st.button("Start Assistant"):
            initialize_assistant()

# Chat interface
if st.session_state.initialized:
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="message-container"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-container"><div class="assistant-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # User input
    user_input = st.text_input("Type your message here...", key="user_input")
    
    if st.button("Send") or user_input:
        if user_input:  # Prevent empty messages
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Process user input and get response
            assistant_response = st.session_state.assistant.process_user_input(user_input)
            
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Clear input box
            st.session_state.user_input = ""
            
            # Force refresh to show new messages
            st.experimental_rerun()

else:
    st.info("Please enter your OpenAI API key in the sidebar to start the assistant.")

# Display current candidate information (for debugging/development)
if st.session_state.initialized and st.session_state.assistant:
    with st.sidebar:
        st.header("Candidate Information")
        candidate_data = st.session_state.assistant.candidate_data
        
        st.write(f"Name: {candidate_data['full_name'] or 'Not provided'}")
        st.write(f"Email: {candidate_data['email'] or 'Not provided'}")
        st.write(f"Phone: {candidate_data['phone'] or 'Not provided'}")
        st.write(f"Experience: {candidate_data['experience'] or 'Not provided'}")
        st.write(f"Position: {candidate_data['desired_position'] or 'Not provided'}")
        st.write(f"Location: {candidate_data['location'] or 'Not provided'}")
        st.write(f"Tech Stack: {candidate_data['tech_stack'] or 'Not provided'}")
        
        st.header("Conversation State")
        st.write(f"Stage: {st.session_state.assistant.state['stage']}")
        st.write(f"Fields Collected: {', '.join(st.session_state.assistant.state['fields_collected'])}")
        
        if st.button("Reset Conversation"):
            st.session_state.initialized = False
            st.session_state.messages = []
            st.session_state.assistant = None
            st.experimental_rerun()
