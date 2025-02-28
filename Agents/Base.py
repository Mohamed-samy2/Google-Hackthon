from abc import ABC
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
class Base(ABC):
    def __init__(self):
        super().__init__()
        
        load_dotenv()
        self.llm =ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.6,
            max_retries=4,
            )
        
        self.memory = InMemorySaver()
        