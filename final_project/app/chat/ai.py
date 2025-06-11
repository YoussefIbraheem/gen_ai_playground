from langchain_ollama import ChatOllama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent , SQLDatabaseToolkit
from langchain_community.agents import ZeroShotAgent
from sqlalchemy import create_engine , inspect
from app import db
from config import Config

def initialize_sql_agent():
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    
    inspector = inspect(engine)
    
    existing_tables = inspector.get_table_names()
    
    sql_db = SQLDatabase.from_uri(
        database_uri= Config.SQLALCHEMY_DATABASE_URI,
        engine=engine,
        sample_rows_in_table_info=2,
        include_tables= existing_tables
    )
    

    llm = ChatOllama(model="llama3.2:3b")
    
    available_tables = existing_tables

    toolkit = SQLDatabaseToolkit(db=sql_db , llm=llm)
    
    prompt = f"""You are a helpful AI assistant that can answer questions about the database. You have access to the following tables: {', '.join(existing_tables)}. Use the SQLDatabaseToolkit to interact with the database.
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
    
    sql_agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        prompt= prompt
    )

