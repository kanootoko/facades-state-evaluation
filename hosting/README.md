# Hosting helpers

These configuration files will help to host a complete solution.

## Basic setup

Firstly you will need to copy `.env.example` file and fill the values inside.
  You may skip EMAIL, DOMAIN and HTTPS_PORT if you do not plan to get ssl certificate.

## HTTP-only hosting

To start nginx in http-mode you will need to run `docker compose -f nginx-http-only.d-c.yml up -d` -
  this will remove all https-related configurations from `nginx.conf` and start it.

Note that you need to start nginx after other containers if you use docker-networks names as proxy destinations.

## Getting SSL certificate from LetsEncrypt

Firstly you need to start HTTP hosting same as above.

Then run `docker compose -f certbot-run-once.d-c.yml --rm` to generate certificate
  (it will be stored in `ssl` directory which then will be mounted)
  and then you can stop http-only version by running `docker compose -f nginx-http-only.d-c down`

## HTTP/HTTPS hosting

After ssl certificate is generated and stored in `ssl` directory, one can run `docker compose up nginx.conf`
  to start proxy services in both http and https modes.
