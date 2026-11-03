import re
from dataclasses import dataclass

@dataclass
class SafetyCheck:
    passed: bool
    reason: str = ""

class AgentSafetyLayer:
    DANGEROUS_PATTERNS = [
        r"rm\s+-rf",
        r"DROP\s+TABLE",
        r"DELETE\s+FROM",
        r"format\s+C:",
        r"sudo\s+",
        r"chmod\s+777",
    ]
    
    def check_action(self, tool_name: str, args: dict) -> SafetyCheck:
        # Check for dangerous commands
        args_str = str(args)
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, args_str, re.IGNORECASE):
                return SafetyCheck(False, f"Dangerous pattern detected: {pattern}")
        
        # Check tool whitelist
        allowed_tools = ["search_web", "write_file", "run_code", "send_email"]
        if tool_name not in allowed_tools:
            return SafetyCheck(False, f"Tool '{tool_name}' not in whitelist")
        
        # Check rate limits per tool
        # (implementation depends on your tracking system)
        
        return SafetyCheck(True)
    
    def check_output(self, output: str) -> SafetyCheck:
        # Check for sensitive data leakage
        sensitive_patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN detected'),
            (r'\b\d{16}\b', 'Credit card number detected'),
            (r'password\s*[:=]\s*\S+', 'Password in output'),
        ]
        
        for pattern, reason in sensitive_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                return SafetyCheck(False, f"Sensitive data in output: {reason}")
        
        return SafetyCheck(True)

safety = AgentSafetyLayer()

# Check before executing tool
check = safety.check_action("run_code", {"code": "import os; os.system('rm -rf /')"})
if not check.passed:
    print(f"BLOCKED: {check.reason}")
