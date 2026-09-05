# Dockerfile for Nginx with Brotli module
# Multi-stage build to keep the final image small

FROM nginx:alpine AS builder

RUN apk add --no-cache --virtual .build-deps \
    gcc make libc-dev pcre-dev zlib-dev git linux-headers

# Clone ngx_brotli
RUN git clone --recursive https://github.com/google/ngx_brotli.git /tmp/ngx_brotli

# Get Nginx source version matching the installed binary
RUN NGINX_VERSION=$(nginx -v 2>&1 | cut -d'/' -f2) \
    && wget -q "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -O /tmp/nginx.tar.gz \
    && tar -xzf /tmp/nginx.tar.gz -C /tmp \
    && cd /tmp/nginx-${NGINX_VERSION} \
    && ./configure --with-compat --add-dynamic-module=/tmp/ngx_brotli \
    && make modules \
    && cp objs/ngx_http_brotli_filter_module.so /tmp/ \
    && cp objs/ngx_http_brotli_static_module.so /tmp/

# Final image
FROM nginx:alpine

COPY --from=builder /tmp/ngx_http_brotli_filter_module.so /etc/nginx/modules/
COPY --from=builder /tmp/ngx_http_brotli_static_module.so /etc/nginx/modules/
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
