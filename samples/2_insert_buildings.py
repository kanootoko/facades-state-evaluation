import json
import sys
import time

import pandas as pd
import sqlalchemy
from sqlalchemy import func, insert
from sqlalchemy.dialects import postgresql
from tqdm import tqdm

tqdm.pandas()

db_addr = "localhost"
db_port = 5432
db_name = "facades_db"
db_user = "postgres"
db_pass = "postgres"

with open("buildings.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame([feature["properties"] | {"geometry": feature["geometry"]} for feature in data["features"]])
print("Read GeoJSON as DataFrame:")
print(df)

from numpy import nan

df["address"] = df["addr:street"].fillna("") + ", " + df["addr:housenumber"].fillna("")
df["address"] = df["address"].apply(lambda addr: addr.strip(", ")).replace({"": None})
df["osm_id"] = df["type_x"] + "/" + df["id"].apply(str)
df = df[["osm_id", "building:year_built", "address", "geometry"]].replace({nan: None})
df = df.rename({"building:year_built": "year"}, axis=1)
df = df.drop_duplicates(subset="osm_id")

print("Buildings prepared for insertion:")
print(df)

try:
    sys.path.append("../backend/")
    from facades_api.db.entities import buildings
except:
    print(
        "Unable to import buildings class from entities of facades_api.db module (facades_api should have been at ../backend directory)"
    )
    raise

filename: str | None
if len(sys.argv) > 1:
    dialect = postgresql.dialect()
    filename = sys.argv[1]
    print(
        f"Attempting to use {filename} as output sql commands filename, no connection to the database will be established."
        " (Ctrl+C to abort, process will begin in 5 seconds)."
    )
    time.sleep(5)
    with open(filename, "wt", encoding="utf-8") as file:
        print("BEGIN TRANSACTION;", file=file)
        def insert_building(building_info: pd.Series) -> bool:
            if building_info["geometry"]["type"] not in ("Point", "Polygon", "MultiPolygon"):
                return False
            try:
                year = int(building_info["year"])
            except:
                year = None
            statement = insert(buildings).values(
                osm_id=building_info["osm_id"],
                address=building_info["address"],
                building_year=year,
                geometry=func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(building_info["geometry"])), 4326),
            )
            print(statement.compile(dialect=dialect, compile_kwargs={"literal_binds": True}), end=";\n", file=file)
            return True

        inserted = df.progress_apply(insert_building, axis=1).astype(int).sum()
        print("COMMIT;", file=file)
else:
    print("Opening connection to the database at postgresql://{db_user}@{db_addr}:{db_port}/{db_name}.")

    engine = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_pass}@{db_addr}:{db_port}/{db_name}")

    inserted = 0
    with engine.connect() as conn:

        def insert_building(building_info: pd.Series) -> bool:
            if building_info["geometry"]["type"] not in ("Point", "Polygon", "MultiPolygon"):
                return False
            try:
                year = int(building_info["year"])
            except:
                year = None
            statement = insert(buildings).values(
                osm_id=building_info["osm_id"],
                address=building_info["address"],
                building_year=year,
                geometry=func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(building_info["geometry"])), 4326),
            )
            conn.execute(statement)
            return True

        try:
            with conn.begin():
                inserted = df.progress_apply(insert_building, axis=1).astype(int).sum()
        finally:
            try:
                conn.close()
            except:
                pass

print(f"Inserted {inserted} buildings.")
