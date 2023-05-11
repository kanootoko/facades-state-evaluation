FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN sed -i '/^\ *ssl.*$/d' /etc/nginx/nginx.conf && \
    sed -i '/^.*ssl;$/d' /etc/nginx/nginx.conf && \
    sed -i '/^\ *ssl_certificate.*$/d' /etc/nginx/nginx.conf && \
    sed -i '/^\ *ssl_certificate_key.*$/d' /etc/nginx/nginx.conf && \
    mkdir -p /ssl/.well-known
