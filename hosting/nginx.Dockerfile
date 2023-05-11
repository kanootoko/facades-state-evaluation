FROM nginx:alpine

ARG DOMAIN=default.domain.com
ARG BACKEND_ADDRESS=http://172.17.0.1:8080

COPY nginx.conf /etc/nginx/nginx.conf

RUN sed -i 's/$(DOMAIN)/'$DOMAIN'/g' /etc/nginx/nginx.conf && \
    sed -i 's,$(BACKEND_ADDRESS),'$BACKEND_ADDRESS',g' /etc/nginx/nginx.conf && \
    \
    echo "16 2 */7 * * nginx -s reload" > /etc/crontabs/certbot && \
    \
    echo "crond" > /entrypoint && \
    echo "nginx -g 'daemon off;'" >> /entrypoint && \
    echo "nginx" >> /entrypoint

ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint"]
