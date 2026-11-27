# nginx.conf — Strangler fig routing: new service for some routes, legacy for others
upstream legacy_app {
    server legacy-app:3000;
}

upstream new_service {
    server new-service:8080;
}

server {
    listen 80;
    server_name api.shop.com;

    # Routes already migrated to the new service
    location /api/v2/customers {
        proxy_pass http://new_service;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    location /api/v2/orders {
        proxy_pass http://new_service;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    # Everything else goes to the legacy app
    location / {
        proxy_pass http://legacy_app;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
