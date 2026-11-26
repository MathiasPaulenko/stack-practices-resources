#!/usr/bin/env bash
# Vault dynamic database credentials: config + role + on-demand read

vault secrets enable database

vault write database/config/my-postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@db:5432/mydb?sslmode=disable" \
    allowed_roles="readonly"

vault write databa
