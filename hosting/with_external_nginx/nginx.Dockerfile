FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN echo "16 2 */7 * * nginx -s reload" > /etc/crontabs/certbot && \
    \
    echo "crond" > /entrypoint && \
    echo "nginx -g 'daemon off;'" >> /entrypoint && \
    echo "nginx" >> /entrypoint

ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint"]
