from .Base import Base
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated,Literal
from googleapiclient.discovery import build
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import re

class CarPrice(BaseModel):
    """The Average Salary of the Cars"""
    cars_avg_salary: int = Field(...,
        description = "The Average price of the car"
    )

class CarState(TypedDict):
    # Main Graph states
    messages : Annotated[list, add_messages]
    # Sub Class States
    car_name: str
    car_model:str
    cars_avg_salary: int
    search_results:str

class CarAgent(Base):
    def __init__(self):
        super().__init__()
        self.llm =ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.4,
            api_key='AIzaSyBMfI-quDrgCwNBFWologuKAkxgPXfiUkI',
            max_retries=2,
            )
        self.api_key="AIzaSyAcabkVCxzNzBK79AJvy3c-RajZxDqlOtU"
        self.search_engine_id = "a613832f9b6c343de"
        
        workflow = StateGraph(CarState)
        workflow.add_node("researcher",self.get_results)
        workflow.add_node("get_salary",self.get_avg_salary)
        
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher","get_salary")
        workflow.add_edge("get_salary",END)
        
        self.graph = workflow.compile(checkpointer=self.memory) 

    def google_search(self, query,**kwargs):

        service = build("customsearch", "v1", developerKey=self.api_key)
        res = service.cse().list(q=query, cx=self.search_engine_id, gl='eg', cr='countryEG', **kwargs).execute()
        return res.get('items', [])
    
    def get_results(self,state:CarState):
        car_name = state["car_name"]
        car_model = state["car_model"]

        search_query = f"{car_name} {car_model} price Egypt"
        # search_results = self..invoke({"query":search_query})
        search_results = self.google_search(search_query, num=10)
        return {'search_results':'\n'.join([item['snippet'] for item in search_results])}
    
    def get_avg_salary(self,state:CarState):
        structured_llm = self.llm.with_structured_output(CarPrice)
        
        sys_prompt = '\n'.join([
            "You are a helpful assistant that helps to get the  average price of the cars",
            "Your task is to get the average price of the given car model in Egypt",
            "Provide the average fees onlyin EGP"
        ])
        
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",sys_prompt),
                ("user", "Search Results: {search_results}"),
            ]
        )
        
        retrieval_grader = grade_prompt | structured_llm
        
        result = retrieval_grader.invoke({'search_results':state["search_results"]})
        return {'cars_avg_salary':result.cars_avg_salary}
    
if "__main__" == __name__:
    agent = CarAgent()
    config = {'configurable':{"thread_id":1}}
    print(agent.graph.invoke({'car_name':'suzuki','car_model':"swift"},config=config)['cars_avg_salary'])

    