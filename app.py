import streamlit as st
from hiring_assistant import HiringAssistant

# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="👨‍💼",
    layout="centered"
)

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

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    if not st.session_state.initialized:
        api_key = st.text_input("Enter your Groq API Key", type="password")
        st.session_state.api_key = api_key
        if st.button("Start Assistant") and api_key:
            initialize_assistant()
            st.rerun()  # Rerun to reflect initialized state
    else:
        if st.button("Reset Conversation"):
            st.session_state.initialized = False
            st.session_state.messages = []
            st.session_state.assistant = None
            st.rerun()

# Chat interface
if st.session_state.initialized:
    # Display chat messages using st.chat_message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input with chat-style input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process input and get response
        with st.spinner("Assistant is thinking..."):
            assistant_response = st.session_state.assistant.process_user_input(prompt)
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
        # Rerun to update the UI
        st.rerun()

    # Display candidate information
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
        st.write(f"Fields Collected: {', '.join(st.session_state.assistant.state['fields_collected']) or 'None'}")
else:
    st.info("Please enter your Groq API key in the sidebar to start the assistant.")
