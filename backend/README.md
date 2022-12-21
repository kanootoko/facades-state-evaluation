# facades_api

## preparation

0. To install python dependencies (if you wish to run script without Docker) run `python -m pip install -r requirements.txt`.  
1. Prepare a PostgreSQL database management server and create an empty database (named `facades_db` by default)
2. Go to ./facades_api/db and run `alembic upgrade head` to apply migrations. Do not forget to set environment variables
  `DB_ADDR`, `DB_PORT`, `DB_NAME`, `DB_USER` and `DB_PASS` if they are different from default values
3. Fill `buildings` table with city buildings geometry from [OSM](https://openstreetmap.org) as shown in [data example](../samples/download_and_insert_buildings.ipynb)

## launching

Run backend locally with `make run`

## run in docker

0. Create .env file by copying and editing [env.example](env.example)
1. Build image with `make docker-build`
2. Run a container with `make docker-run` (.env file variables will be used by Docker)

As an alternative, one can use built image as `docker run kanootoko/facades_api:latest`.

## configuration

You can change backend configuration by editing .env flie (got from `env.example`) or pass arguments as command-line parameters.  
Run `python -m facades_api --help` to get help.
