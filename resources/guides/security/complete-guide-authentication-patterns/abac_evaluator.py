"""RBAC map + ABAC policy evaluator with $subject.* placeholder resolution.

Source: https://stackpractices.com/guides/complete-guide-authentication-patterns/
"""
from enum import Enum


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


ROLE_PERMISSIONS = {
    "viewer": {Permission.READ},
    "editor": {Permission.READ, Permission.WRITE},
    "admin": {Permission.READ, Permission.WRITE, Permission.DELETE,
              Permission.ADMIN},
}


def check_rbac(user_role: str, required_permission: Permission) -> bool:
    return required_permission in ROLE_PERMISSIONS.get(user_role, set())


class ABACEvaluator:
    def __init__(self):
        self.policies = []

    def add_policy(self, policy: dict):
        self.policies.append(policy)

    def evaluate(self, subject: dict, resource: dict, action: str) -> bool:
        for policy in self.policies:
            if self._match(policy, subject, resource, action):
                return policy["effect"] == "allow"
        return False  # default deny

    def _resolve(self, expected, subject: dict):
        """Resolve placeholders like '$subject.id' against the real subject."""
        if isinstance(expected, str) and expected.startswith("$subject."):
            return subject.get(expected[len("$subject."):])
        return expected

    def _match(self, policy: dict, subject: dict,
               resource: dict, action: str) -> bool:
        if action not in policy.get("actions", []):
            return False
        for key, value in policy.get("subject", {}).items():
            if subject.get(key) != self._resolve(value, subject):
                return False
        for key, value in policy.get("resource", {}).items():
            if resource.get(key) != self._resolve(value, subject):
                return False
        return True
