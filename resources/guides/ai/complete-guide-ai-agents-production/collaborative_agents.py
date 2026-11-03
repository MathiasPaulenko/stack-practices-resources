class CollaborativeAgents:
    def __init__(self, agents: dict[str, str], model: str = "gpt-4o", max_rounds: int = 5):
        self.agents = agents  # name -> system_prompt
        self.model = model
        self.max_rounds = max_rounds
    
    def discuss(self, topic: str) -> list[dict]:
        """Multiple agents discuss a topic and reach consensus."""
        conversation = [{"role": "user", "content": f"Topic for discussion: {topic}"}]
        messages_log = []
        
        for round_num in range(self.max_rounds):
            for agent_name, system_prompt in self.agents.items():
                messages = [
                    {"role": "system", "content": system_prompt},
                    *conversation
                ]
                
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                reply = response.choices[0].message.content
                conversation.append({"role": "assistant", "content": f"[{agent_name}]: {reply}"})
                messages_log.append({"round": round_num + 1, "agent": agent_name, "message": reply})
        
        return messages_log

# Example: Code review discussion
agents = {
    "security_reviewer": "You are a security expert. Review code for vulnerabilities.",
    "performance_reviewer": "You are a performance expert. Review code for bottlenecks.",
    "style_reviewer": "You are a code style expert. Review code for readability and conventions."
}

collab = CollaborativeAgents(agents)
discussion = collab.discuss("Review this code: def process(data): return [d*2 for d in data if d > 0]")
for msg in discussion:
    print(f"[Round {msg['round']}] {msg['agent']}: {msg['message'][:100]}...")
