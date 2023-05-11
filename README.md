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
3. Follow [README.md in hosting directory](hosting/README.md) to configure a HTTP certificate.
4. Configure other environment variables as you need.
5. Run `docker compose up` (or `docker compose -f external-nginx.d-c.yml` if you used external-nginx in step 3)

## How to export all docker images and import them at the server side

If for some reason you can't build images on the final machine, you can build them anywhere else and transfer. Be aware
  that image have huge size because of YOLO dependencies. About 5Gb in total.

1. Build images with `docker compose build`
2. Export images `docker save facades_classifier:latest facades_backend:latest facades_nginx:latest facades_cetrificates_updater:latest -o export/facades-images.tar`
5. Load images on different machine using `docker load -i export/facades-images.tar`