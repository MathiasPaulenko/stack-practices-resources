from dataclasses import dataclass, field

@dataclass
class AgentMemory:
    max_messages: int = 20
    messages: list = field(default_factory=list)
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            # Keep system message + recent messages
            system = [m for m in self.messages if m["role"] == "system"]
            non_system = [m for m in self.messages if m["role"] != "system"]
            self.messages = system + non_system[-(self.max_messages - len(system)):]
    
    def get_messages(self) -> list:
        return self.messages
    
    def clear(self):
        system = [m for m in self.messages if m["role"] == "system"]
        self.messages = system
