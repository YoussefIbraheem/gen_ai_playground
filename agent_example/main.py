from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from datetime import datetime
import requests


llm = ChatOllama(model="llama3.2:3b")


@tool
def get_datetime() -> str:
    """
    Returns the current local date and time as a formatted string.

        The returned string follows the format 'YYYY-MM-DD HH:MM:SS', representing
        the year, month, day, hour, minute, and second.

            str: The current date and time formatted as 'YYYY-MM-DD HH:MM:SS'.

        Example:
            >>> get_datetime()
            '2024-06-12 15:30:45'
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_wiki(query: str) -> str:
    """
    Searches Wikipedia for a given query and returns the summary extract.
    Args:
        query (str): The title of the Wikipedia page to search for.
    Returns:
        str: The summary extract of the Wikipedia page.
    Raises:
        ValueError: If the page cannot be loaded or any other exception occurs.
    Example:
        summary = search_wiki("Python_(programming_language)")
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract")
        else:
            raise ValueError(f"Trouble Loading Page for {query}")
    except Exception as exc:
        raise ValueError(f"{exc}")


@tool
def math_calculation(expression: str) -> str:
    """
    Evaluates a mathematical expression provided as a string and returns the result as a string.

    Args:
        expression (str): A mathematical expression to be evaluated, e.g., "2 + 2 * 3".

    Returns:
        str: The result of the evaluated expression.

    Example:
        >>> math_calculation("5 * (3 + 2)")
        '25'

    Note:
        This tool is intended for use by LLM agents to perform arithmetic calculations based on user input.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as exc:
        return "Invalid math expression"


tools = [get_datetime, search_wiki, math_calculation]

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "you're an assitant that answers question with the help of wikipedia and other tools given",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def search_agent_chat(query: str):
    response = executor.invoke({"input": query, "chat_history": []})

    return response["output"]


search_agent_chat("Tell me more about AI")
