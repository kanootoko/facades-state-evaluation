import json
import sys

import pandas as pd
import sqlalchemy
from sqlalchemy import func, insert
from tqdm import tqdm

db_addr = "localhost"
db_port = 5432
db_name = "facades_db"
db_user = "postgres"
db_pass = "postgres"

with open("buildings.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame([feature["properties"] | {"geometry": feature["geometry"]} for feature in data["features"]])
print(df)

from numpy import nan

df["address"] = df["addr:street"].fillna("") + ", " + df["addr:housenumber"].fillna("")
df["address"] = df["address"].apply(lambda addr: addr.strip(", ")).replace({"": None})
df = df[["id", "building:year_built", "address", "geometry"]].replace({nan: None})
df = df.drop_duplicates(subset="id")
print(df)


sys.path.append("../backend/")
from facades_api.db.entities import buildings

engine = sqlalchemy.create_engine(f"postgresql://{db_user}:{db_pass}@{db_addr}:{db_port}/{db_name}")

number_skipped = 0
with engine.connect() as conn:
    try:
        with conn.begin():
            for _, (osm_id, year, address, geometry) in tqdm(
                df.iterrows(), total=df.shape[0], desc="buildings insertion"
            ):
                if geometry["type"] not in ("Point", "Polygon", "Multipolygon"):
                    number_skipped += 1
                    continue
                try:
                    year = int(year)
                except:
                    year = None
                statement = insert(buildings).values(
                    osm_id=osm_id,
                    address=address,
                    building_year=year,
                    geometry=func.ST_SetSRID(func.ST_GeomFromGeoJSON(json.dumps(geometry)), 4326),
                )
                conn.execute(statement)
    finally:
        try:
            conn.close()
        except:
            pass

print(f"Inserted {df.shape[0] - number_skipped} buildings")
