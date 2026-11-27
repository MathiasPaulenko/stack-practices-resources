# Restart nginx to refresh OCSP stapling
nginx -t && systemctl restart nginx
