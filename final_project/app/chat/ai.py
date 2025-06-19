from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor, create_sql_agent
from sqlalchemy import create_engine, inspect
from app import db
from config import Config


def initialize_sql_agent():

    print("Initializing SQL Agent...")
    print(f"Using database URI: {Config.SQLALCHEMY_DATABASE_URI}")

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

    inspector = inspect(engine)

    existing_tables = inspector.get_table_names()

    available_tables = existing_tables

    sql_db = SQLDatabase.from_uri(
        Config.SQLALCHEMY_DATABASE_URI,
        include_tables=available_tables,
        sample_rows_in_table_info=5,
    )

    llm = ChatOllama(model="llama3.2:3b")

    toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)

    # prompt = f"""You are a helpful AI assistant that can answer questions about the database. You have access to the following tables: {available_tables}. Use the SQLDatabaseToolkit to interact with the database.
    # * CRITICAL INSTRUCTIONS:
    # 1. Never Mention SQL Query or SQL Database in your response.
    # 2. Always respond in a conversational manner.
    # 3. Never mention the name of the database or the tables in your response.
    # """
    
    # prompt is disabled as llam3.2:3b is not compatible with custom prompts and require an LLM that supports ReAct
    
    # prompt_template = PromptTemplate.from_template(
    #     prompt,
    #     partial_variables={
    #         "existing_tables": ", ".join(existing_tables),
    #         "available_tables": ", ".join(available_tables),
    #         "tools": toolkit.get_tools(),
    #         "tools_names": toolkit.get_tools(),
    #         "tool_names": toolkit.get_tools(),
    #         "agent_scratchpad": "",
    #     },
    # )

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        input_variables=["input"],
    )
    
    agent.handle_parsing_errors = True

    print("SQL Agent initialized successfully.")
    return agent
