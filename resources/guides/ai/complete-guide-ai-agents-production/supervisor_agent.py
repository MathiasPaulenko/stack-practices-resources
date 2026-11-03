from openai import OpenAI
import json

client = OpenAI()

class SupervisorAgent:
    def __init__(self, sub_agents: dict, model: str = "gpt-4o"):
        self.sub_agents = sub_agents
        self.model = model
    
    def delegate(self, task: str) -> dict:
        """Decide which sub-agent(s) to use for the task."""
        agent_descriptions = "\n".join(
            f"- {name}: {desc}" for name, desc in self.sub_agents.items()
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a supervisor. Delegate tasks to the appropriate agent.\n\nAvailable agents:\n{agent_descriptions}\n\nReturn JSON: {{\"agent\": \"name\", \"task\": \"specific task for the agent\"}}"
                },
                {"role": "user", "content": task}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def run(self, task: str) -> str:
        delegation = self.delegate(task)
        agent_name = delegation["agent"]
        sub_task = delegation["task"]
        
        # In production, route to actual sub-agent implementation
        return f"Delegated to {agent_name}: {sub_task}"

# Define sub-agents
sub_agents = {
    "research_agent": "Searches the web and gathers information",
    "code_agent": "Writes, tests, and debugs code",
    "writer_agent": "Writes reports, documentation, and content",
    "data_agent": "Analyzes data and creates visualizations"
}

supervisor = SupervisorAgent(sub_agents)
result = supervisor.run("Write a Python script to analyze sales data and create a report")
print(result)
