# utils.py
import hashlib
import re
import os
import json
from datetime import datetime

def sanitize_input(text):
    """
    Sanitize user input to prevent any potential security issues.
    Remove harmful characters and scripts.
    """
    if not text:
        return ""
    
    # Remove potentially dangerous HTML/script tags
    sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    sanitized = re.sub(r'<.*?>', '', sanitized)
    
    return sanitized.strip()

def validate_email(email):
    """Validate email format."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.match(email_pattern, email))

def validate_phone(phone):
    """Validate phone number format."""
    # This is a simplified version - real validation would be more complex
    phone_pattern = r'\b(?:\+\d{1,3}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
    return bool(re.match(phone_pattern, phone))

def hash_sensitive_data(data):
    """Hash sensitive data for storage (for demo purposes)."""
    if not data:
        return None
    return hashlib.sha256(data.encode()).hexdigest()

def secure_store_candidate(candidate_data, store_plaintext=False):
    """
    Store candidate data securely.
    In a real app, this would interact with a secure database with proper encryption.
    """
    # Create a copy to avoid modifying the original
    secure_data = candidate_data.copy()
    
    # Hash sensitive information if not storing plaintext
    if not store_plaintext:
        if secure_data.get("email"):
            secure_data["email_hash"] = hash_sensitive_data(secure_data["email"])
            secure_data["email"] = f"{secure_data['email'][0]}***@{secure_data['email'].split('@')[1]}"
        
        if secure_data.get("phone"):
            secure_data["phone_hash"] = hash_sensitive_data(secure_data["phone"])
            secure_data["phone"] = "***-***-" + secure_data["phone"][-4:] if len(secure_data["phone"]) >= 4 else "***"
    
    # Add timestamp
    secure_data["stored_at"] = datetime.now().isoformat()
    
    # Generate filename from candidate name or use UUID if name not available
    filename = None
    if secure_data.get("full_name"):
        safe_name = "".join(c for c in secure_data["full_name"] if c.isalnum() or c.isspace()).replace(" ", "_").lower()
        filename = f"secure_candidates/{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    else:
        import uuid
        filename = f"secure_candidates/candidate_{uuid.uuid4().hex}.json"
    
    # Ensure directory exists
    os.makedirs("secure_candidates", exist_ok=True)
    
    # Write to file
    with open(filename, "w") as f:
        json.dump(secure_data, f, indent=2)
    
    return filename
