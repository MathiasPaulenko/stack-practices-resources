"""Generated-file snapshot example.

Snapshot tests are a good fit for generated artifacts: the baseline
captures the exact output and any drift in the generator shows up
as a reviewable diff instead of a broken deploy.
"""


def generate_nginx_config(domain: str, ssl: bool, upstream: str) -> str:
    lines = [
        "server {",
        "    listen 80;",
        f"    server_name {domain};",
        "",
        "    location / {",
        f"        proxy_pass http://{upstream};",
        "        proxy_set_header Host $host;",
        "    }",
    ]
    if ssl:
        lines += [
            "",
            "    listen 443 ssl;",
            f"    ssl_certificate     /etc/letsencrypt/live/{domain}/fullchain.pem;",
            f"    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;",
        ]
    lines.append("}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(generate_nginx_config(domain="example.com", ssl=True, upstream="localhost:3000"))
