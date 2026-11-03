from enum import Enum
from typing import Optional

class ApprovalStatus(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class HumanInTheLoopAgent:
    def __init__(self, tools: dict, require_approval_for: list[str]):
        self.tools = tools
        self.require_approval_for = require_approval_for
        self.pending_actions: list[dict] = []
    
    def propose_action(self, tool_name: str, args: dict) -> dict:
        """Propose an action for human approval."""
        action = {"tool": tool_name, "args": args, "status": "pending"}
        
        if tool_name in self.require_approval_for:
            self.pending_actions.append(action)
            return {"status": "needs_approval", "action": action}
        else:
            # Auto-approve safe tools
            result = self.tools[tool_name](**args)
            return {"status": "executed", "result": result}
    
    def approve_action(self, action_id: int, status: ApprovalStatus, modified_args: dict = None) -> dict:
        """Human approves, rejects, or modifies an action."""
        action = self.pending_actions[action_id]
        
        if status == ApprovalStatus.REJECTED:
            action["status"] = "rejected"
            return {"status": "rejected"}
        
        args = modified_args or action["args"]
        result = self.tools[action["tool"]](**args)
        action["status"] = "executed"
        action["result"] = result
        return {"status": "executed", "result": result}
    
    def get_pending(self) -> list[dict]:
        return [a for a in self.pending_actions if a["status"] == "pending"]

# Usage
agent = HumanInTheLoopAgent(
    tools={"send_email": lambda **k: f"Email sent to {k.get('to')}", "search": lambda **k: "results"},
    require_approval_for=["send_email"]
)

# Agent proposes sending an email
result = agent.propose_action("send_email", {"to": "boss@company.com", "subject": "Report", "body": "Here is the report."})
print(result)  # {"status": "needs_approval", ...}

# Human approves
approval = agent.approve_action(0, ApprovalStatus.APPROVED)
print(approval)  # {"status": "executed", "result": "Email sent to boss@company.com"}
