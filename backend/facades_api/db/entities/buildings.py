# pylint: disable=too-many-ancestors, abstract-method
"""
Buildings database table is defined here.
"""
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Sequence, String, Table, UniqueConstraint, Numeric, text, Float

from facades_api.db import metadata


buildings_id_seq = Sequence("buildings_id_seq")

buildings = Table(
    "buildings",
    metadata,
    Column("id", Integer, buildings_id_seq, server_default=buildings_id_seq.next_value(), primary_key=True),
    Column("osm_id", String(20)),
    Column("address", String(256)),
    Column("building_year", Integer),
    Column("geometry", Geometry(srid=4326), nullable=False),
    Column("evaluation", Numeric(5, 3), server_default=text("null")),
    Column("evaluation_raw", Float, server_default=text("null")),
    UniqueConstraint("osm_id", name="buildings_unique_osm_id"),
)
"""
Buildings from OpenStreetMap.

Columns:
- `id` - building identifier, int serial
- `osm_id` - OpenStreetMap identifier, varchar(20)
- `address` - building address, varchar(256)
- `building_year` - year the building was built, int
- `geometry` - building geometry, Geometry
- `evaluation` - building facades evaluation value, numeric(5, 3)
- `evaluation_raw` - building facades evaluation value, float
"""
