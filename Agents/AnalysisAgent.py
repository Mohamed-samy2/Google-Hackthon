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
    club_avg_salary: int
    cars_avg_salary: int
    avg_fees: int
    
    suggestions:str

class AnalysisAgent(Base):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the CSV file
        file_path = os.path.join(current_dir, "credit_data_processed.csv")
        self.data = pd.read_csv(file_path)

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
        client_data = self.data[self.data["Name"] == state['client_name']]
        old_data_str = "\n".join([f"{col}: {client_data.iloc[0][col]}" for col in client_data.columns])
        return {'old_data':old_data_str}
    
    def get_new_data(self,state:Analysis_State):
        
        return {'new_data': f"""
                        Consistency of Work & Gigs: 10
                        Freelancing Experience (years) : 2
                        Income Diversification : 4.5
                        Financial Risk Events : 2.5
                        FICO Score : 500
                        Credit Score : 80000
                        IScore : 450
                        Interest Rate (%) : 0
                        Loan Eligibility : 1
                        Car Average Price :{state['cars_avg_salary']}
                        Club Average Price :{state['club_avg_salary']}
                        University Average Fees :{state['avg_fees']}
                        """
                }
    
    def get_response(self,state:Analysis_State):

        sys_prompt = '\n'.join([
            "**You are an AI assistant that speaks with very simple , clear language for an installment platform that provides dynamic credit and installment plans to customers**.",
            "when the customer fainancial status improved you should suggest to increase the installment and vise versa, increase or decrease the installments with logical amounts with respect to the customer status update and don't exceed the following given limits (+ or - 2k), assume that the current installment is 8k.",
            "Your role is to:",
            "1) Analyze customer data in a simple, clear format.",
            '2) Adjust the installment amount dynamically based on financial changes while keeping it within an acceptable range (+ or - 2k).',
            "3) Update the installment plan if the customer's financial situation changes, such as:",
            '- Taking multiple jobs this month',
            '- Increase or decrease in income', 
            '- provide me the detailes.'          
        ])
        
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",sys_prompt),
                ("user", '\n'.join(['### Customer Data:',
                '*Old Data:*',
                '{old_data_str}',
                '*Updated Data:*',
                '{updated_data_str}',
                '### Expected Output:',
                '- Summarized customer data (clear and simple)'])),
            ]
        )
        
        retrieval_grader = grade_prompt | self.llm
        
        result = retrieval_grader.invoke({'old_data_str':state['old_data'],'updated_data_str':state['new_data']})

        return {'suggestions':result}
    
if "__main__" == __name__:
    agent = AnalysisAgent()
    config = {'configurable':{"thread_id":1}}
    print(agent.graph.invoke({'client_name':7},config=config)['suggestions'].content)