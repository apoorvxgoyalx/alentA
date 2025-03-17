# TalentScout Hiring Assistant

A conversational AI chatbot for initial candidate screening in tech recruitment, built using Streamlit and Large Language Models (LLMs).

## Features

- **Interactive Chat Interface**: Engaging, professional conversation with candidates
- **Information Collection**: Gathers essential candidate details systematically
- **Tech Stack Assessment**: Generates relevant technical questions based on candidate's declared skills
- **Context-Aware Conversations**: Maintains conversation flow and follows up appropriately
- **Data Security**: Handles candidate information securely
- **User-Friendly UI**: Clean, intuitive Streamlit interface

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (or other compatible LLM API key)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Access the application in your browser at `http://localhost:8501`

### Configuration

- When you first start the application, you'll be prompted to enter your API key
- The key is stored only in the session and not persisted between application restarts

## Using the Hiring Assistant

1. **Starting a Conversation**: The assistant will greet candidates and explain its purpose
2. **Information Collection**: It will systematically collect the following information:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Desired Position(s)
   - Current Location
   - Tech Stack
3. **Technical Assessment**: Based on the tech stack, relevant technical questions will be asked
4. **Conversation Conclusion**: The assistant will thank the candidate and explain next steps

## System Architecture

- **Frontend**: Streamlit-based user interface
- **Backend**:
  - LangChain for LLM orchestration
  - OpenAI API for natural language processing
  - State management for conversation flow
- **Data Handling**:
  - Local JSON storage for candidate information
  - Secure handling of sensitive information

## Deployment Options

### Local Deployment
The application is configured for local deployment by default, which is ideal for development and testing.

### Cloud Deployment
For production use, the application can be deployed to cloud platforms:

1. **Streamlit Cloud**:
   - Create a `secrets.toml` file for API key storage
   - Push to a GitHub repository
   - Connect to Streamlit Cloud

2. **Heroku**:
   - Add a `Procfile` with: `web: streamlit run app.py`
   - Configure environment variables for API keys
   - Deploy using Heroku CLI or GitHub integration

3. **AWS/GCP/Azure**:
   - Deploy as a containerized application using Docker
   - Set up environment variables for configuration
   - Configure networking and security settings

## Security Considerations

- API keys are stored only in memory during the session
- Sensitive candidate information is hashed before storage
- No persistent database connection in the demo version
- Production deployment should implement additional security measures

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using Streamlit and LangChain
- Powered by OpenAI's language models