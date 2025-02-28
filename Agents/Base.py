from abc import ABC,abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

class Base(ABC):
    def __init__(self):
        super().__init__()
        
        self.llm =ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.6,
            api_key='AIzaSyBqwAc1lQu01M72g4CcFSiqQ_j48du4ZwU',
            max_retries=4,
            )
        
        self.memory = InMemorySaver()
        