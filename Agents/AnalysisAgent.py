from .Base import Base
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict,Annotated,Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import TavilySearchResults
import os
import pandas as pd



class Analysis_State(TypedDict):
    # Main Graph states
    messages : Annotated[list, add_messages]
    # Sub Class States
    client_name: int
    old_data:str
    new_data:str
    
    suggestions:str

class AnalysisAgent(Base):
    def __init__(self):
        super().__init__()
        self.data = pd.read_csv(r"C:\Users\Dell\Desktop\Google hackthon\Google-Hackthon\Agents\credit_data.csv")
        

        workflow = StateGraph(Analysis_State)
        workflow.add_node("get_client_data",self.get_client_data)
        workflow.add_node("get_new_data",self.get_new_data)
        workflow.add_node("get_response",self.get_response)
        
        workflow.set_entry_point("get_client_data")
        workflow.add_edge("get_client_data","get_new_data")
        workflow.add_edge("get_new_data","get_response")
        workflow.add_edge("get_response",END)
        
        self.graph = workflow.compile(checkpointer=self.memory)
    
    def get_client_data(self,state:Analysis_State):
        client_data = self.data[self.data["Customer Name"] == state['client_name']]
        old_data_str = "\n".join([f"{col}: {client_data.iloc[0][col]}" for col in client_data.columns])
        print(old_data_str)
        return {'old_data':old_data_str}
    
    def get_new_data(self,state:Analysis_State):
        
        return {'new_data': """
                        (Manually enter updated values here)
                        Income: 15000
                        Spending: 6500
                        Installment: 8900
                        """
                }
        
    
    def get_response(self,state:Analysis_State):

        sys_prompt = '\n'.join([
            "You are an AI assistant for an installment platform that provides dynamic credit and installment plans to customers.",
            "Your role is to:",
            "1) Analyze customer data and summarize it in a simple, clear format.",
            '2) Adjust the installment amount dynamically based on financial changes while keeping it within an acceptable range (±2K).',
            '3) Update the installment plan if the customer’s financial situation changes, such as:',
            '- Taking multiple jobs this month',
            '- Increase or decrease in income',
            '- Changes in spending habits',
            '### Customer Data:',
            '*Old Data:*',
            '{old_data_str}',
            '*Updated Data:*',
            '{updated_data_str}',
            '### Expected Output:',
            '- Summarized customer data (clear and simple).',
            '- New recommended installment amount with reasoning.'
        ])
        
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",sys_prompt),
                ("user", ''),
            ]
        )
        
        retrieval_grader = grade_prompt | self.llm
        
        result = retrieval_grader.invoke({'old_data_str':state['old_data'],'updated_data_str':state['new_data']})
        
        return {'suggestions':result}
    


if "__main__" == __name__:
    agent = AnalysisAgent()
    config = {'configurable':{"thread_id":1}}
    print(agent.graph.invoke({'client_name':1},config=config)['suggestions'])