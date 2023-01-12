FROM alpine

ARG EMAIL=default@email.com
ARG DOMAIN=default.domain.com

RUN apk add certbot

RUN echo "cd /ssl" > /usr/bin/update_certificate && \
    echo "/usr/bin/certbot renew --quiet" >> /usr/bin/update_certificate && \
    echo "cp -rL /etc/letsencrypt/live/* /ssl/" >> /usr/bin/update_certificate && \
    \
    mkdir -p /etc/letsencrypt /ssl/.well-known && \
    \
    echo "authenticator = webroot" > /etc/letsencrypt/cli.ini && \
    echo "webroot-path = /ssl/" >> /etc/letsencrypt/cli.ini && \
    echo "text = True" >> /etc/letsencrypt/cli.ini && \
    \
    echo "15 2 */7 * * certbot renew --quiet" > /etc/crontabs/certbot && \
    \
    echo "crond -f" > /run_with_cron && \
    echo "certbot certonly -d "$DOMAIN > /run_once && \
    echo "cp -rL /etc/letsencrypt/live/* /ssl/" > /run_once && \
    chmod +x /usr/bin/update_certificate

RUN echo 'Y' | certbot register --email $EMAIL

ENTRYPOINT ["/bin/sh"]
CMD ["/run_with_cron"]
