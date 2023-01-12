FROM nginx:alpine

ARG BACKEND_ADDRESS=http://172.17.0.1:8080

COPY nginx.conf /etc/nginx/nginx.conf

RUN sed -i 's,$(BACKEND_ADDRESS),'$BACKEND_ADDRESS',g' /etc/nginx/nginx.conf && \
    sed -i '/^\ *ssl.*$/d' /etc/nginx/nginx.conf && \
    sed -i '/^.*ssl;$/d' /etc/nginx/nginx.conf && \
    sed -i '/^\ *server_name.*$/d' /etc/nginx/nginx.conf && \
    sed -i '/^\ *ssl_certificate.*$/d' /etc/nginx/nginx.conf && \
    sed -i '/^\ *ssl_certificate_key.*$/d' /etc/nginx/nginx.conf && \
    mkdir -p /ssl/.well-known
