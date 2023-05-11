FROM alpine

ARG EMAIL
ARG DOMAIN

RUN apk add certbot bash

RUN echo "cd /ssl" > /usr/bin/update_certificate && \
    echo "certbot renew --quiet" >> /usr/bin/update_certificate && \
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
    echo "echo 'running with cron'" > /run_with_cron && \
    echo "mv /etc/letsencrypt.bak/cli.ini /etc/letsencrypt/cli.ini" >> /run_with_cron && \
    echo "crond -f" >> /run_with_cron && \
    \
    echo "echo 'running once'" > /run_once && \
    echo "mv /etc/letsencrypt.bak/cli.ini /etc/letsencrypt/cli.ini" >> /run_once && \
    echo "certbot certonly -d "$DOMAIN >> /run_once && \
    echo "cp -rL /etc/letsencrypt/live/* /ssl/" >> /run_once && \
    chmod +x /usr/bin/update_certificate

RUN certbot register --email $EMAIL --non-interactive --agree-tos

RUN cp -r /etc/letsencrypt /etc/letsencrypt.bak

ENTRYPOINT ["/bin/sh"]
CMD ["/run_with_cron"]
