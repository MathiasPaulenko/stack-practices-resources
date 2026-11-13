"""Minimal RBAC evaluator in pure stdlib Python.

Companion code for https://stackpractices.com/recipes/implement-rbac/

Roles form a hierarchy via `parent`. A user inherits the permissions of
all their roles plus everything those roles inherit. Checks deny by
default: anything not explicitly granted returns False.

Usage:
    python check_rbac.py --demo            # built-in roles + scenarios
    python check_rbac.py roles.json checks.json   # your own data
"""

import json
import sys

DEFAULT_ROLES = {
    "viewer": {
        "parent": None,
        "permissions": ["orders:read", "reports:read"],
    },
    "editor": {
        "parent": "viewer",
        "permissions": ["orders:write", "products:read"],
    },
    "admin": {
        "parent": "editor",
        "permissions": [
            "users:read", "users:write", "users:delete", "settings:write",
        ],
    },
}

DEFAULT_USERS = {
    "ana@example.com": ["admin"],
    "beto@example.com": ["editor"],
    "carol@example.com": ["viewer"],
}


class Rbac:
    def __init__(self, roles):
        self.roles = roles

    def role_permissions(self, role_name, seen=None):
        """All permissions of a role, walking up the parent chain."""
        seen = seen or set()
        role = self.roles.get(role_name)
        if role is None or role_name in seen:
            return set()
        seen.add(role_name)
        perms = set(role["permissions"])
        if role.get("parent"):
            perms |= self.role_permissions(role["parent"], seen)
        return perms

    def has_permission(self, user_roles, resource, action):
        needle = f"{resource}:{action}"
        for role_name in user_roles:
            if needle in self.role_permissions(role_name):
                return True
        return False


def main():
    if len(sys.argv) == 3:
        roles = json.load(open(sys.argv[1], encoding="utf-8"))
        checks = json.load(open(sys.argv[2], encoding="utf-8"))
    else:
        roles = DEFAULT_ROLES
        checks = [
            {"user": "ana@example.com", "resource": "users", "action": "delete"},
            {"user": "beto@example.com", "resource": "orders", "action": "write"},
            {"user": "beto@example.com", "resource": "orders", "action": "read"},
            {"user": "carol@example.com", "resource": "orders", "action": "write"},
            {"user": "carol@example.com", "resource": "reports", "action": "read"},
        ]

    rbac = Rbac(roles)
    users = DEFAULT_USERS if len(sys.argv) != 3 else checks.get("users", {})

    for check in checks if isinstance(checks, list) else checks["checks"]:
        email = check["user"]
        decision = rbac.has_permission(
            users.get(email, []), check["resource"], check["action"]
        )
        granted = f"{check['resource']}:{check['action']}"
        print(f"{email} -> {granted}: {'ALLOW' if decision else 'DENY'}")


if __name__ == "__main__":
    main()
