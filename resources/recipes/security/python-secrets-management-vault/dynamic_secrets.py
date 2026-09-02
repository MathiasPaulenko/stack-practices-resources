"""Dynamic database credentials via the Vault database secrets engine."""
from __future__ import annotations

import hvac


def enable_database_engine(vault: hvac.Client) -> None:
    """Enable the database secrets engine at the default path."""
    vault.sys.enable_secrets_engine(
        backend_type="database",
        path="database",
    )


def configure_postgresql(
    vault: hvac.Client,
    connection_url: str,
    username: str,
    password: str,
    allowed_roles: str = "app-role",
) -> None:
    """Configure a PostgreSQL connection for the database secrets engine."""
    vault.write("database/config/my-postgresql", {
        "plugin_name": "postgresql-database-plugin",
        "allowed_roles": allowed_roles,
        "connection_url": connection_url,
        "username": username,
        "password": password,
    })


def create_role(
    vault: hvac.Client,
    role_name: str = "app-role",
    db_name: str = "my-postgresql",
    default_ttl: str = "1h",
    max_ttl: str = "24h",
) -> None:
    """Create a role that generates PostgreSQL users with SELECT grants."""
    vault.write(f"database/roles/{role_name}", {
        "db_name": db_name,
        "creation_statements": [
            "CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}';",
            "GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";",
        ],
        "default_ttl": default_ttl,
        "max_ttl": max_ttl,
    })


def get_dynamic_db_credentials(vault: hvac.Client, role_path: str = "database/creds/app-role") -> dict:
    """Request a fresh set of dynamic database credentials."""
    response = vault.read(role_path)
    return {
        "username": response["data"]["username"],
        "password": response["data"]["password"],
        "lease_id": response["lease_id"],
        "lease_duration": response["lease_duration"],
        "renewable": response["renewable"],
    }


if __name__ == "__main__":
    from vault_client import create_vault_client

    vault = create_vault_client()

    enable_database_engine(vault)
    configure_postgresql(
        vault,
        connection_url="postgresql://{{username}}:{{password}}@db.example.com:5432/mydb",
        username="vault_admin",
        password="vault_admin_password",
    )
    create_role(vault)

    creds = get_dynamic_db_credentials(vault)
    print(f"Dynamic user: {creds['username']}")
    print(f"Lease duration: {creds['lease_duration']}s")
