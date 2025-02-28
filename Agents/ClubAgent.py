from .Base import Base
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import TavilySearchResults
import os
class club_avg_output(BaseModel):
    
    """The Average Salary of the Club"""
    avg_salary: int = Field(...,
        description = "The Average Salary of the Club"
    )

class Club_State(TypedDict):
    # Main Graph states
    messages : Annotated[list, add_messages]
    # Sub Class States
    club_name: str
    club_avg_salary: int
    search_results:str



class ClubAgent(Base):
    
    def __init__(self):
        super().__init__()
        
        self.search =  TavilySearchResults(
        max_results=15,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        description="Get a detailed prices for club memberships",
        )
        
        workflow = StateGraph(Club_State)
        workflow.add_node("researcher",self.get_results)
        workflow.add_node("get_salary",self.get_avg_salary)
        
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher","get_salary")
        workflow.add_edge("get_salary",END)
        
        self.graph = workflow.compile(checkpointer=self.memory) 
    
    def get_results(self,state:Club_State):
        club_name = state["club_name"]
        prompt = f"What is the price of the memberships of {club_name}."
        search_results = self.search.invoke({"query":prompt})
        return {'search_results':'\n'.join([result['content'] for result in search_results])}
    
    
    def get_avg_salary(self,state:Club_State):
        structured_llm = self.llm.with_structured_output(club_avg_output)
        
        sys_prompt = '\n'.join([
            "You are a helpful assistant that helps to get the average price memberships of a club",
            "Your task is to get the average price of the memberships of a club",
            "provide the average price only"
        ])
        
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",sys_prompt),
                ("user", "Search Results: {search_results}"),
            ]
        )
        
        retrieval_grader = grade_prompt | structured_llm
        
        result = retrieval_grader.invoke({'search_results':state["search_results"]})
        
        return {'club_avg_salary':result.avg_salary}
    


if "__main__" == __name__:
    agent = ClubAgent()
    config = {'configurable':{"thread_id":1}}
    print(agent.graph.invoke({'club_name':'el ahly club'},config=config)['club_avg_salary'])
    