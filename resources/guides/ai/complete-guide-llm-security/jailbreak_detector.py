"""Heuristic jailbreak signal - pairs with the injection guard."""
import re


class JailbreakDetector:
    JAILBREAK_PATTERNS = [
        r"DAN|do\s+anything\s+now",
        r"pretend\s+(you\s+are|to\s+be)\s+.*(evil|unrestricted|jailbroken)",
        r"translate.*?(ignore|forget|override).*?instructions",
        r"(I\s+am|this\s+is)\s+(the|your)\s+(admin|developer|owner)",
        r"what\s+are\s+your\s+(rules|instructions|restrictions)",
    ]

    def detect(self, user_input: str) -> dict:
        lower = user_input.lower()
        for pattern in self.JAILBREAK_PATTERNS:
            # IGNORECASE matters: patterns contain capitals but input is lowercased
            if re.search(pattern, lower, re.IGNORECASE):
                return {"is_jailbreak": True, "pattern": pattern, "severity": "high"}
        if len(user_input) > 10000:
            return {"is_jailbreak": True, "pattern": "excessive_length", "severity": "medium"}
        return {"is_jailbreak": False}
