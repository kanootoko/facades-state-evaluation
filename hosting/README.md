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

## Using external Nginx with subdomains

Another possible solution is to configure an outer nginx to proxy all requests from domain/subdomain to facades Nginx.
  Certificates must be used by the outer Nginx, so the best solution is to run it inside the Docker itself, but in
  the different network. Same applies to other services.
  
The workflow is following:

- create network `hosting_net` and volumes `facades_ssl` and `facades_letsencrypt`
- change `nginx.conf` by setting your domain and other services if needed
- get certificates for facades service and your other services:
  - run docker-compose for file `with_external_nginx/nginx-http-only.c-c.yml`
  - run docker-compose for file `with_external_nginx/certbot-run-once.d-c.yml` with set DOMAIN and EMAIL
    environment variables for a service
  - (repeat for all your services)
  - stop nginx-http-only docker-compose and remove its resources among with certbot-run-once
- run docker-compose for file external-nginx.d-c.yml in the root of the project

To add more services to this configuration, you will need to:

1. Add service subdomain and proxy path inside the `hosting_net` docker network to with_external_nginx/nginx.conf
2. Add a mock service with the same name to with_external_nginx/certbot-run-once.d-c.yml
3. Run docker-compose file with_external_nginx/certbot-run-once.d-c.yml for the service
4. Rebuild and restart nginx.d-c.yml