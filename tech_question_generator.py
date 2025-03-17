from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Dictionary mapping technologies to their domains
TECHNOLOGY_DOMAINS = {
    "python": "programming_language",
    "java": "programming_language",
    "javascript": "programming_language",
    "typescript": "programming_language",
    "c#": "programming_language",
    "ruby": "programming_language",
    "go": "programming_language",
    "php": "programming_language",
    "react": "frontend_framework",
    "angular": "frontend_framework",
    "vue": "frontend_framework",
    "svelte": "frontend_framework",
    "django": "backend_framework",
    "flask": "backend_framework",
    "spring": "backend_framework",
    "laravel": "backend_framework",
    "express": "backend_framework",
    "node": "backend_framework",
    "mysql": "database",
    "postgresql": "database",
    "mongodb": "database",
    "redis": "database",
    "sql server": "database",
    "oracle": "database",
    "docker": "devops",
    "kubernetes": "devops",
    "jenkins": "devops",
    "aws": "cloud",
    "azure": "cloud",
    "gcp": "cloud",
    "git": "version_control",
    "terraform": "infrastructure",
    "react native": "mobile",
    "flutter": "mobile",
    "swift": "mobile",
    "kotlin": "mobile"
}

class TechQuestionGenerator:
    def __init__(self, llm):
        """Initialize the tech question generator with an LLM."""
        self.llm = llm
        
        # Create template for generating questions
        self.question_template = PromptTemplate(
            input_variables=["tech_stack", "difficulty_level"],
            template="""
            Generate {difficulty_level} technical questions to assess a candidate's proficiency in the following technologies: {tech_stack}
            
            For each technology, create 1-2 questions that:
            1. Assess real-world knowledge and practical application (not just syntax)
            2. Cannot be easily answered with a simple Google search
            3. Reveal the depth of the candidate's understanding
            4. Are specific to the technology mentioned
            5. Can be answered concisely in a chat format (not requiring code samples)
            
            Format each question with a clear indication of which technology it's testing.
            """
        )
        
        self.question_chain = LLMChain(
            llm=self.llm,
            prompt=self.question_template,
            verbose=True
        )
    
    def parse_tech_stack(self, tech_stack_text):
        """
        Parse the tech stack text to identify known technologies.
        Returns a dictionary grouped by domain.
        """
        # Convert to lowercase for easier matching
        text_lower = tech_stack_text.lower()
        
        # Initialize results
        tech_domains = {}
        
        # Check for each known technology
        for tech, domain in TECHNOLOGY_DOMAINS.items():
            if tech in text_lower:
                if domain not in tech_domains:
                    tech_domains[domain] = []
                tech_domains[domain].append(tech)
        
        return tech_domains
    
    def generate_questions(self, tech_stack, num_questions=5):
        """
        Generate technical questions based on the candidate's tech stack.
        Returns a list of questions.
        """
        # Parse tech stack to identify technologies by domain
        tech_domains = self.parse_tech_stack(tech_stack)
        
        # Prepare the tech stack string for the prompt
        tech_stack_formatted = ", ".join([tech for domain in tech_domains.values() for tech in domain])
        if not tech_stack_formatted:
            tech_stack_formatted = tech_stack  # Use original if no matches found
        
# Generate different difficulty questions
        basic_questions = self.question_chain.run(
            tech_stack=tech_stack_formatted,
            difficulty_level="basic"
        )
        
        advanced_questions = self.question_chain.run(
            tech_stack=tech_stack_formatted,
            difficulty_level="advanced"
        )
        
        # Parse questions from the responses
        # In a production system, you'd need more robust parsing
        all_questions = []
        
        # Simple parsing by line breaks and filtering
        basic_lines = [line.strip() for line in basic_questions.split("\n") if line.strip()]
        advanced_lines = [line.strip() for line in advanced_questions.split("\n") if line.strip()]
        
        # Filter lines that look like questions (ending with ?)
        for line in basic_lines + advanced_lines:
            if line.endswith("?") and len(line) > 10:  # Simple heuristic for questions
                all_questions.append(line)
        
        # Limit to requested number, but ensure at least one question if any generated
        return all_questions[:num_questions] if all_questions else ["Could you describe your experience with " + tech_stack_formatted + "?"]
    
    def generate_follow_up_question(self, tech_stack, previous_question, previous_answer):
        """
        Generate a follow-up question based on the candidate's previous answer.
        This provides more dynamic conversation flow.
        """
        follow_up_template = PromptTemplate(
            input_variables=["tech_stack", "previous_question", "previous_answer"],
            template="""
            Based on the candidate's answer to a technical question about {tech_stack}, generate a relevant follow-up question.
            
            Previous question: {previous_question}
            Candidate's answer: {previous_answer}
            
            The follow-up question should:
            1. Dig deeper into the topic based on their response
            2. Test a related but different aspect of the technology
            3. Be more specific if their previous answer was very general
            4. Assess practical application if their previous answer was theoretical
            
            Generate ONE natural follow-up question that a skilled technical interviewer would ask.
            """
        )
        
        follow_up_chain = LLMChain(
            llm=self.llm,
            prompt=follow_up_template,
            verbose=True
        )
        
        return follow_up_chain.run(
            tech_stack=tech_stack,
            previous_question=previous_question,
            previous_answer=previous_answer
        ).strip()
