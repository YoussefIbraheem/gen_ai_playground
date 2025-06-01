from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b")


db = SQLDatabase.from_uri("sqlite:///shop.db")

def create_simple_sql_agent():
    toolkit = SQLDatabaseToolkit(db=db,llm=llm)
    agent_executer = create_sql_agent(
        llm= llm,
        toolkit=toolkit,
        verbose=True,
        agent_type= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors= True
    )
    
    return agent_executer


agent = create_simple_sql_agent()



def chat_w_db(query:str):
    response = agent.invoke(query)
    return response


chat_w_db("How many customers do we have?")