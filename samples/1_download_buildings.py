import requests
import osm2geojson
import geopandas as gpd
import pandas as pd

city_name = "Санкт-Петербург"
overpass_url = "http://overpass-api.de/api/interpreter"

overpass_query = """
[out:json];
        area[name="{city_name}"]->.searchArea;
        (
             relation[building](area.searchArea);
             way[building](area.searchArea);
        );
out geom;
""".format(
    city_name=city_name
)

result = requests.get(overpass_url, params={"data": overpass_query}).json()
resp = osm2geojson.json2geojson(result)
buildings_osm = gpd.GeoDataFrame.from_features(resp["features"]).set_crs(4326)
for column in buildings_osm.columns:
    buildings_osm[column] = buildings_osm[column].apply(lambda x: x[0] if isinstance(x, list) else x)
buildings_osm = pd.merge(
    buildings_osm.drop("tags", axis=1), pd.DataFrame(list(buildings_osm["tags"])), left_index=True, right_index=True
)
print(buildings_osm)
print("Saving to file 'buildings.geojson'")
buildings_osm.to_file("buildings.geojson", driver="GeoJSON")
