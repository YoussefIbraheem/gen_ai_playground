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

    prompt = f"""You are a helpful AI assistant that can answer questions about the database. You have access to the following tables: {available_tables}. Use the SQLDatabaseToolkit to interact with the database.
    * CRITICAL INSTRUCTIONS:
    1. Never Mention SQL Query or SQL Database in your response.
    2. Always respond in a conversational manner.
    3. Never mention the name of the database or the tables in your response.
    4. Always provide a direct answer to the user's question.
    5. If the user asks for a list of tables, columns, or any other metadata, politely decline and say you can only answer questions about the data in the tables.
    6. Do not provide any information about the database structure, such as table names or column names.
    7. Do not run any SQL queries that are not directly related to answering the user's question.
    
    * AVAILABLE DATA TABLES TO BE ACCESSIBLE BY YOU ONLY: {available_tables}
    
    * RESPONSE TEMPLATES:
    - for counts: **Metric**: [Number] [context]
    -for percentage: **Metric**: [Number]% [context]
    - for averages: **Metric**: [Number] [context]
    - for sums: **Metric**: [Number] [context]
    - for revenue: **Metric**: [Number] [context]
    - for currency: **Metric**: [Number] [context]
    - for profit: **Metric**: [Number] [context]
    """

    prompt_template = PromptTemplate.from_template(
        prompt,
        handle_parsing_errors=True,
        partial_variables={
            "existing_tables": ", ".join(existing_tables),
            "available_tables": ", ".join(available_tables),
            "tools": toolkit.get_tools(),
            "tools_names": toolkit.get_tools(),
            "tool_names": toolkit.get_tools(),
            "agent_scratchpad": "",
            "input": "{input}",
        },
    )

    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        prompt=prompt_template,
        verbose=True,
    )
    
    agent.handle_parsing_errors = True

    print("SQL Agent initialized successfully.")
    return agent
