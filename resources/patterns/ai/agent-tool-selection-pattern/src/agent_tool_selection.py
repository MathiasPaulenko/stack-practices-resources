from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
import re

@dataclass
class Tool:
    name: str
    description: str
    category: str
    parameters: Dict[str, str] = field(default_factory=dict)

@dataclass
class AgentState:
    task: str
    phase: str = "planning"
    history: List[str] = field(default_factory=list)
    available_tools: List[str] = field(default_factory=list)

# Tool registry
TOOL_REGISTRY: Dict[str, Tool] = {
    "web_search": Tool(
        "web_search", "Search the web for information", "research",
        {"query": "string", "max_results": "int"}
    ),
    "code_search": Tool(
        "code_search", "Search the codebase for patterns", "research",
        {"pattern": "string", "language": "string"}
    ),
    "read_file": Tool(
        "read_file", "Read file contents", "file_ops",
        {"path": "string"}
    ),
    "write_file": Tool(
        "write_file", "Write content to a file", "file_ops",
        {"path": "string", "content": "string"}
    ),
    "run_tests": Tool(
        "run_tests", "Execute test suite", "execution",
        {"test_file": "string", "filter": "string"}
    ),
    "deploy": Tool(
        "deploy", "Deploy application to environment", "execution",
        {"environment": "string", "version": "string"}
    ),
    "calculator": Tool(
        "calculator", "Perform mathematical calculations", "utility",
        {"expression": "string"}
    ),
    "sql_query": Tool(
        "sql_query", "Execute SQL query on database", "data",
        {"query": "string", "database": "string"}
    ),
}

# Phase-based tool mapping
PHASE_TOOLS: Dict[str, List[str]] = {
    "planning": ["web_search", "code_search", "calculator"],
    "implementation": ["read_file", "write_file", "code_search"],
    "testing": ["read_file", "run_tests", "code_search"],
    "deployment": ["run_tests", "deploy", "read_file"],
    "analysis": ["sql_query", "calculator", "web_search"],
}

def select_tools_by_phase(state: AgentState) -> List[Tool]:
    """Select tools based on the current agent phase."""
    tool_names = PHASE_TOOLS.get(state.phase, [])
    return [TOOL_REGISTRY[name] for name in tool_names if name in TOOL_REGISTRY]

def select_tools_by_keywords(state: AgentState) -> List[Tool]:
    """Select tools based on keyword matching in the task."""
    text = (state.task + " " + " ".join(state.history)).lower()

    keyword_map = {
        "search|find|look up|research": ["web_search", "code_search"],
        "read|open|view|inspect": ["read_file"],
        "write|create|modify|update|edit": ["write_file", "read_file"],
        "test|spec|assert|validate": ["run_tests", "read_file"],
        "deploy|release|publish|ship": ["deploy", "run_tests"],
        "calculate|compute|math|sum|average": ["calculator"],
        "query|database|sql|select|join": ["sql_query"],
    }

    selected: set = set()
    for pattern, tools in keyword_map.items():
        if re.search(pattern, text):
            selected.update(tools)

    if not selected:
        selected.update(PHASE_TOOLS.get(state.phase, ["web_search"]))

    return [TOOL_REGISTRY[name] for name in selected if name in TOOL_REGISTRY]

class ToolSelector:
    def __init__(self, strategy: str = "phase"):
        self.strategy = strategy

    def select(self, state: AgentState) -> List[Tool]:
        if self.strategy == "phase":
            return select_tools_by_phase(state)
        elif self.strategy == "keyword":
            return select_tools_by_keywords(state)
        else:
            return list(TOOL_REGISTRY.values())

    def format_tools_for_prompt(self, tools: List[Tool]) -> str:
        """Format tool definitions for inclusion in LLM prompt."""
        lines = []
        for tool in tools:
            params = ", ".join(f"{k}: {v}" for k, v in tool.parameters.items())
            lines.append(f"- {tool.name}({params}): {tool.description}")
        return "\n".join(lines)

# Usage
if __name__ == "__main__":
    state = AgentState(
        task="Find all Python files with SQL injection vulnerabilities and fix them",
        phase="implementation",
        history=["Found 3 files with raw SQL queries"],
    )

    selector = ToolSelector(strategy="keyword")
    tools = selector.select(state)

    print(f"Selected {len(tools)} tools:")
    for t in tools:
        print(f"  {t.name}: {t.description}")

    print("\nFormatted for prompt:")
    print(selector.format_tools_for_prompt(tools))
