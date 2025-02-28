from .Base import Base
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
import os

os.environ["TAVILY_API_KEY"] = "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"

class uni_avg_output(BaseModel):
    
    """The Average Salary of the Club"""
    avg_fees: int = Field(...,
        description = "The Average fees of the college in University"
    )

class Uni_State(TypedDict):
    # Main Graph states
    messages : Annotated[list, add_messages]
    # Sub Class States
    uni_name: str
    college_name:str
    avg_fees: int
    search_results:str

class UniversityAgent(Base):
    def __init__(self):
        super().__init__()
        self.llm =ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.4,
            api_key='AIzaSyBMfI-quDrgCwNBFWologuKAkxgPXfiUkI',
            max_retries=2,
            )
        
        self.search =  TavilySearchResults(
        max_results=15,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        )
        
        workflow = StateGraph(Uni_State)
        workflow.add_node("researcher",self.get_results)
        workflow.add_node("get_salary",self.get_avg_salary)
        
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher","get_salary")
        workflow.add_edge("get_salary",END)
        
        self.graph = workflow.compile(checkpointer=self.memory) 
    
    def get_results(self,state:Uni_State):
        uni_name = state["uni_name"]
        college_name = state["college_name"]
        prompt = f"What is the average egyptian tuition fees for faculty of {college_name} in {uni_name} University in Egypt for Egyptain Students per semester."
        search_results = self.search.invoke({"query":prompt})
        return {'search_results':'\n'.join([result['content'] for result in search_results])}
    
    def get_avg_salary(self,state:Uni_State):
        structured_llm = self.llm.with_structured_output(uni_avg_output)
        
        sys_prompt = '\n'.join([
            "You are a helpful assistant that helps to get the  average egyptian tuition fees for a faculty in a given university in Egypt",
            "Your task is to get the average egyptian tuition fees for a faculty in a given university in Egypt",
            "provide the average fees onlyin EGP"
        ])
        
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",sys_prompt),
                ("user", "Search Results: {search_results}"),
            ]
        )
        
        retrieval_grader = grade_prompt | structured_llm
        
        result = retrieval_grader.invoke({'search_results':state["search_results"]})
        return {'avg_fees':result.avg_fees}
    
if "__main__" == __name__:
    agent = UniversityAgent()
    config = {'configurable':{"thread_id":1}}
    print(agent.graph.invoke({'uni_name':'Ain Shams','college_name':"Engineering"},config=config)['avg_fees'])
