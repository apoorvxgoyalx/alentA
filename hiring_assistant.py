# At the top of hiring_assistant.py
import os
import json
from datetime import datetime
import uuid
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
# ... rest of your imports
from prompts import (
    SYSTEM_PROMPT,
    GREETING_PROMPT,
    INFO_GATHERING_PROMPT,
    TECH_QUESTION_PROMPT,
    FOLLOW_UP_PROMPT,
    CLOSING_PROMPT,
    FALLBACK_PROMPT
)

class HiringAssistant:
    def __init__(self, api_key):
        """Initialize the hiring assistant with API key and conversation state."""
        # os.environ[""] = api_key
        os.environ["OPENAI_API_KEY"] = ""

        # Initialize the language model
        self.llm = OpenAI(temperature=0.7)
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(return_messages=True, output_key="output")
        
        # Create chains for different conversation stages
        self.greeting_chain = LLMChain(
            llm=self.llm,
            prompt=GREETING_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        self.info_gathering_chain = LLMChain(
            llm=self.llm,
            prompt=INFO_GATHERING_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        self.tech_question_chain = LLMChain(
            llm=self.llm,
            prompt=TECH_QUESTION_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        self.follow_up_chain = LLMChain(
            llm=self.llm,
            prompt=FOLLOW_UP_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        self.closing_chain = LLMChain(
            llm=self.llm,
            prompt=CLOSING_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        self.fallback_chain = LLMChain(
            llm=self.llm,
            prompt=FALLBACK_PROMPT,
            verbose=True,
            memory=self.memory,
            output_key="output"
        )
        
        # Initialize candidate data structure
        self.candidate_data = {
            "full_name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "desired_position": None,
            "location": None,
            "tech_stack": None,
            "conversation_log": [],
            "technical_responses": []
        }
        
        # Conversation state management
        self.state = {
            "stage": "greeting",  # greeting, info_gathering, tech_questions, closing
            "fields_collected": [],
            "current_question": 0,
            "total_questions": 0,
            "questions_asked": []
        }
    
    def extract_information(self, user_input):
        """
        Extract candidate information from user input using pattern matching and NLP.
        This is a simplified version - in a production system, you would use more 
        sophisticated NLP techniques or entity extraction.
        """
        # This is a placeholder for more sophisticated information extraction
        # In a real system, you would use NER models or regex patterns
        
        # Simple email extraction
        import re
        
        # Email pattern
        if not self.candidate_data["email"] and "email" not in self.state["fields_collected"]:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_match = re.search(email_pattern, user_input)
            if email_match:
                self.candidate_data["email"] = email_match.group(0)
                self.state["fields_collected"].append("email")
        
        # Phone pattern
        if not self.candidate_data["phone"] and "phone" not in self.state["fields_collected"]:
            phone_pattern = r'\b(?:\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
            phone_match = re.search(phone_pattern, user_input)
            if phone_match:
                self.candidate_data["phone"] = phone_match.group(0)
                self.state["fields_collected"].append("phone")
        
        # For other fields, we'll rely on the conversation flow to collect them explicitly
        # This is because free-form text requires more context to properly extract information
    
    def get_remaining_fields(self):
        """Get the list of fields that still need to be collected."""
        all_fields = ["full_name", "email", "phone", "experience", "desired_position", "location", "tech_stack"]
        return [field.replace("_", " ").title() for field in all_fields if field not in self.state["fields_collected"]]
    
    def update_conversation_log(self, role, content):
        """Update the conversation log with a new message."""
        self.candidate_data["conversation_log"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def process_user_input(self, user_input):
        """Process user input based on current conversation state and return assistant response."""
        # Check for exit commands
        exit_commands = ["exit", "quit", "bye", "goodbye", "end"]
        if user_input.lower() in exit_commands or any(cmd in user_input.lower() for cmd in exit_commands):
            return "Thank you for your time. The conversation has been ended. Have a great day!"
        
        # Extract any information from the input
        self.extract_information(user_input)
        
        # Update conversation log
        self.update_conversation_log("user", user_input)
        
        # Get chat history for context
        chat_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.candidate_data["conversation_log"]])
        
        # Process based on current stage
        if self.state["stage"] == "greeting":
            # After greeting, move to info gathering
            if "full_name" not in self.state["fields_collected"] and any(word in user_input.lower() for word in ["hello", "hi", "hey", "greetings"]):
                # Still in greeting phase
                response = self.greeting_chain.run(chat_history=chat_history)
            else:
                # Extract name from first response if possible
                self.candidate_data["full_name"] = user_input
                self.state["fields_collected"].append("full_name")
                self.state["stage"] = "info_gathering"
                remaining_fields = self.get_remaining_fields()
                response = self.info_gathering_chain.run(
                    chat_history=chat_history,
                    remaining_fields=", ".join(remaining_fields)
                )
        
        elif self.state["stage"] == "info_gathering":
            # Check if we've collected all required information
            remaining_fields = self.get_remaining_fields()
            
            # Update fields based on latest response
            if "email" not in self.state["fields_collected"] and "@" in user_input:
                self.candidate_data["email"] = user_input
                self.state["fields_collected"].append("email")
            elif "phone" not in self.state["fields_collected"] and any(c.isdigit() for c in user_input):
                self.candidate_data["phone"] = user_input
                self.state["fields_collected"].append("phone")
            elif "experience" not in self.state["fields_collected"] and any(c.isdigit() for c in user_input) and "year" in user_input.lower():
                self.candidate_data["experience"] = user_input
                self.state["fields_collected"].append("experience")
            elif "desired_position" not in self.state["fields_collected"]:
                self.candidate_data["desired_position"] = user_input
                self.state["fields_collected"].append("desired_position")
            elif "location" not in self.state["fields_collected"]:
                self.candidate_data["location"] = user_input
                self.state["fields_collected"].append("location")
            elif "tech_stack" not in self.state["fields_collected"]:
                self.candidate_data["tech_stack"] = user_input
                self.state["fields_collected"].append("tech_stack")
            
            # Check if we've collected all fields
            if len(self.get_remaining_fields()) == 0:
                # Move to technical questions
                self.state["stage"] = "tech_questions"
                response = self.tech_question_chain.run(
                    chat_history=chat_history,
                    tech_stack=self.candidate_data["tech_stack"]
                )
                self.state["current_question"] = 1
                self.state["total_questions"] = 3  # Default to 3 questions
            else:
                # Continue gathering information
                response = self.info_gathering_chain.run(
                    chat_history=chat_history,
                    remaining_fields=", ".join(remaining_fields)
                )
        
        elif self.state["stage"] == "tech_questions":
            # Record technical response
            self.candidate_data["technical_responses"].append({
                "question_number": self.state["current_question"],
                "response": user_input
            })
            
            # Check if we've asked all questions
            if self.state["current_question"] >= self.state["total_questions"]:
                # Move to closing
                self.state["stage"] = "closing"
                response = self.closing_chain.run(
                chat_history=chat_history,
                candidate_name=self.candidate_data["full_name"]
                )
            else:
                # Ask next technical question
                self.state["current_question"] += 1
                response = self.follow_up_chain.run(
                    chat_history=chat_history,
                    tech_stack=self.candidate_data["tech_stack"],
                    question_number=self.state["current_question"],
                    total_questions=self.state["total_questions"]
                )
        
        elif self.state["stage"] == "closing":
            # After closing, any additional input will get a standard response
            response = "Thank you again for your time. A recruiter from TalentScout will be in touch soon if your profile matches our current openings."
        
        else:
            # Fallback for unexpected states
            response = self.fallback_chain.run(
                chat_history=chat_history,
                current_stage=self.state["stage"]
            )
        
        # Update conversation log with assistant response
        self.update_conversation_log("assistant", response)
        
        # Save candidate data to disk
        self.save_candidate_data()
        
        return response
    
    def save_candidate_data(self):
        """Save candidate data to a JSON file."""
        if self.candidate_data["full_name"]:
            # Create a safe filename from candidate name
            safe_name = "".join(c for c in self.candidate_data["full_name"] if c.isalnum() or c.isspace()).replace(" ", "_").lower()
            filename = f"candidates/{safe_name}_{uuid.uuid4().hex[:8]}.json"
            
            # Ensure directory exists
            os.makedirs("candidates", exist_ok=True)
            
            # Write data to file
            with open(filename, "w") as f:
                json.dump(self.candidate_data, f, indent=2)

    def get_conversation_history(self):
        """Return the conversation history for display purposes."""
        return self.candidate_data["conversation_log"]