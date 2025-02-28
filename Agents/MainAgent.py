from .Base import Base
from .CarAgent import CarAgent
from .ClubAgent import ClubAgent
from .UniversityAgent import UniversityAgent
from .AnalysisAgent import AnalysisAgent
from langgraph.graph import StateGraph,END,START
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

class MainState(TypedDict):
    # Main Graph states
    messages : Annotated[list, add_messages]
    club_name: str
    club_avg_salary: int
    car_name: str
    car_model:str
    cars_avg_salary: int
    uni_name: str
    college_name:str
    avg_fees: int
    client_name:int
    
    suggestions:str


class MainAgent(Base):
    def __init__(self):
        super().__init__()
        self.club_agent = ClubAgent()
        self.car_agent = CarAgent()
        self.uni_agent = UniversityAgent()
        self.analysis_agent = AnalysisAgent()

        workflow = StateGraph(MainState)
        workflow.add_node("club_agent",self.club_agent.graph)
        workflow.add_node("car_agent",self.car_agent.graph)
        workflow.add_node("university_agent", self.uni_agent.graph)
        workflow.add_node("analysis_agent", self.analysis_agent.graph)

        workflow.add_edge(START,"club_agent")
        workflow.add_edge(START,"car_agent")
        workflow.add_edge(START,"university_agent")
        workflow.add_edge("club_agent","analysis_agent")
        workflow.add_edge("car_agent","analysis_agent")
        workflow.add_edge("university_agent","analysis_agent")


        self.graph = workflow.compile(checkpointer=self.memory)

    
if "__main__" == __name__:
    agent = MainAgent()
    config = {'configurable':{"thread_id":1}}
    input = {"club_name":"el ahly club",
              "car_name":"suzuki",
              "car_model":"swift",
              "uni_name":"Ain Shams",
              "college_name":"Engineering",
              'client_name':1
             }
    result = agent.graph.invoke(input,config=config)
    print(result['suggestions'].content)