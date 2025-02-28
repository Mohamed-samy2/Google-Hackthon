from abc import ABC,abstractmethod
from langchain_google_genai import ChatGoogleGenerativeAI
# from Configs import get_settings
from langgraph.checkpoint.memory import InMemorySaver

class Base(ABC):
    def __init__(self):
        super().__init__()
        
        self.llm =ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.4,
            api_key='AIzaSyBMfI-quDrgCwNBFWologuKAkxgPXfiUkI',
            max_retries=2,
            )
        
        self.memory= InMemorySaver()
        