from openai import OpenAI
import json
from typing import Callable

client = OpenAI()

class ReActAgent:
    def __init__(self, tools: dict[str, Callable], model: str = "gpt-4o", max_iterations: int = 10):
        self.tools = tools
        self.model = model
        self.max_iterations = max_iterations
        self.tool_schemas = self._build_tool_schemas()
    
    def _build_tool_schemas(self) -> list[dict]:
        schemas = []
        for name, func in self.tools.items():
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or f"Tool: {name}",
                    "parameters": getattr(func, "params", {"type": "object", "properties": {}})
                }
            })
        return schemas
    
    def run(self, task: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are an autonomous agent. Use tools to complete the task. "
                           "Think step by step. If a tool fails, try a different approach."
            },
            {"role": "user", "content": task}
        ]
        
        for i in range(self.max_iterations):
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tool_schemas,
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            messages.append(msg)
            
            if msg.tool_calls:
                for call in msg.tool_calls:
                    func_name = call.function.name
                    func_args = json.loads(call.function.arguments)
                    
                    # Execute tool
                    try:
                        result = self.tools[func_name](**func_args)
                    except Exception as e:
                        result = f"Error: {e}"
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": str(result)
                    })
            else:
                # No tool calls — agent is done
                return msg.content
        
        return "Max iterations reached without completion."

# Define tools
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for '{query}': Result 1, Result 2, Result 3"

def write_file(filename: str, content: str) -> str:
    """Write content to a file."""
    return f"File '{filename}' written successfully ({len(content)} bytes)"

def run_code(code: str) -> str:
    """Execute Python code and return the output."""
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return "Code executed successfully"
    except Exception as e:
        return f"Execution error: {e}"

# Create agent
agent = ReActAgent(
    tools={"search_web": search_web, "write_file": write_file, "run_code": run_code}
)

result = agent.run("Search for Python best practices and write a summary to a file called 'best_practices.txt'")
print(result)
