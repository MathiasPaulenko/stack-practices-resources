"""Tool-calling agent with bounded loop — never run an unbounded agent in prod."""
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from asteval import Interpreter


@tool
def search_database(query: str) -> str:
    """Search the product database for items matching the query."""
    return f"Found 3 products matching '{query}': Widget A, Widget B, Widget C"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression like '15 * 23'."""
    try:
        return str(Interpreter()(expression))
    except Exception as e:
        return f"Error: {e}"


tools = [search_database, calculate]
model = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(model, tools, prompt)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5,
    max_execution_time=60,
    handle_parsing_errors=True,
)

if __name__ == "__main__":
    print(executor.invoke({"input": "Search for 'widget' and compute 15 * 23"})["output"])
