# data

Here lies the examples of some useful stuff

## requirements.txt

This is a list of needed python packages (install with `python -m pip install -r requirements.txt`).
Some remarks:

- Geopandas is harder to install on Windows, you may wish to user [Visual Studio Code](https://code.visualstudio.com/) with `Dev Containers` extension
- Psycopg2 may not install without manipulations with system. You can either solve its problems (e.g. install libpq-dev and python-dev for Ubuntu) or install `psycopg2-binary`

## 1_download_buildings.py

This is a python script to download and save to file buildings from OSM for a given city (Saint-Petersburg is set to city_name variable on top of the code) -
  this may take a while, even a few hours. Geopandas is needed to process geometry. RAM usage can be extremely high too, same applies to the output file (2.6Gb for Saint-Petersburg)

## 2_insert_buildings.py

This is a python script to read buildings geojson and insert its content to PostgreSQL database. Can be run without geopandas.  
It uses up to 15 Gb of RAM to read and process data of Saint-Petersburg, for example.


If you give a parameter to the insertion script, it will be treated as the output filename, sql inserts will be written there.  
Then you can use it like `docker run --rm --network facades-state-evaluation_default -v "$PWD"/samples/insertion.sql:/insertion.sql -e PGPASSWORD=facades_api_password postgres:14 psql -h facades_db facades_db facades_api -f /insertion.sql >/dev/null`
  to insert data in the database running inside Docker container.