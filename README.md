# Facades state evaluation service

The service is ment to be used to run a website for citizens to add images with the deffects of their city
  historical buildings facades and get their state evaluation value which is comparable with others buildings
  facades state evaluations.

## How to run service-by-service

1. Configure and start backend service ([View README.md in backend directory](backend/README.md))
2. Configure and start frontend service (yet to release...)

## How to run all together (docker with docker compose)

1. Get a hosting and domain address for HTTPS support.
2. Clone this repository to your server.
3. Configure .env file in `hosting` and get LetsEncrypt certificate ([View README.md in hosting directory](hosting/README.md)).
4. Configure other environment variables as you need.
5. Run `docker compose up`