import time
import json
from uuid import uuid4
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentTrace:
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    events: list = field(default_factory=list)
    
    def log(self, event_type: str, **kwargs):
        self.events.append({
            "timestamp": time.time(),
            "type": event_type,
            **kwargs
        })
    
    def log_thought(self, thought: str):
        self.log("thought", content=thought)
    
    def log_action(self, tool: str, args: dict, result: Any):
        self.log("action", tool=tool, args=args, result=str(result)[:500])
    
    def log_error(self, error: str):
        self.log("error", error=error)
    
    def summary(self) -> dict:
        actions = [e for e in self.events if e["type"] == "action"]
        errors = [e for e in self.events if e["type"] == "error"]
        thoughts = [e for e in self.events if e["type"] == "thought"]
        
        duration = 0
        if len(self.events) >= 2:
            duration = self.events[-1]["timestamp"] - self.events[0]["timestamp"]
        
        return {
            "trace_id": self.trace_id,
            "total_events": len(self.events),
            "thoughts": len(thoughts),
            "actions": len(actions),
            "errors": len(errors),
            "duration_seconds": duration,
            "tools_used": list(set(e["tool"] for e in actions)),
        }
    
    def export(self) -> str:
        return json.dumps(self.events, indent=2)

# Usage in agent
trace = AgentTrace()
trace.log_thought("I need to search for information about Python frameworks")
trace.log_action("search_web", {"query": "Python web frameworks"}, "Found: Django, Flask, FastAPI")
trace.log_thought("Now I'll compare them")
trace.log_action("write_file", {"filename": "comparison.txt"}, "File written")
print(trace.summary())
