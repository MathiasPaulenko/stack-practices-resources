from openai import OpenAI
import json

client = OpenAI()

class PlanExecuteAgent:
    def __init__(self, tools: dict, model: str = "gpt-4o"):
        self.tools = tools
        self.model = model
    
    def plan(self, task: str) -> list[dict]:
        """Break down the task into steps."""
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Break down the task into concrete steps. Return JSON array of steps."},
                {"role": "user", "content": f"Task: {task}"}
            ],
            response_format={"type": "json_object"}
        )
        
        data = json.loads(response.choices[0].message.content)
        return data.get("steps", [])
    
    def execute_step(self, step: str, context: str = "") -> str:
        """Execute a single step using tools if needed."""
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"Execute this step. Previous results: {context}"},
                {"role": "user", "content": f"Step: {step}"}
            ]
        )
        return response.choices[0].message.content
    
    def run(self, task: str) -> dict:
        # Phase 1: Plan
        steps = self.plan(task)
        
        # Phase 2: Execute
        results = []
        context = ""
        
        for i, step in enumerate(steps):
            step_desc = step.get("description", str(step))
            result = self.execute_step(step_desc, context)
            results.append({"step": step_desc, "result": result})
            context += f"\nStep {i+1}: {step_desc}\nResult: {result}"
        
        return {"plan": steps, "results": results}

agent = PlanExecuteAgent(tools={})
result = agent.run("Research Python web frameworks, compare them, and write a recommendation report")
