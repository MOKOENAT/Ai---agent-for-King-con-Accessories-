import os
from openai import OpenAI
from data_store import db

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AgentCore:
    def __init__(self):
        self.faqs = db.faqs
        
    def handle_query(self, user_input, user_name="Guest"):
        # Your code here
        return {"response": "Test response", "type": "faq"}

agent = AgentCore()
