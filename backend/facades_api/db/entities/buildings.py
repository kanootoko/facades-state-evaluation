# pylint: disable=too-many-ancestors, abstract-method
"""
Buildings database table is defined here.
"""
from typing import NamedTuple

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, Sequence, String, Table, UniqueConstraint, Numeric, text

from facades_api.db import metadata


class BuildingsTable(Table):
    """
    An attempt to annotate buildings columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "BuildingsColumns",
            [
                ("id", int),
                ("osm_id", int),
                ("address", str),
                ("building_year", int),
                ("geometry", Geometry),
            ],
        )
    }


buildings_id_seq = Sequence("buildings_id_seq")

buildings = BuildingsTable(
    "buildings",
    metadata,
    Column("id", Integer, buildings_id_seq, server_default=buildings_id_seq.next_value(), primary_key=True),
    Column("osm_id", String(20)),
    Column("address", String(256)),
    Column("building_year", Integer),
    Column("geometry", Geometry(srid=4326), nullable=False),
    Column("evaluation", Numeric(4, 3), server_default=text("null")),
    UniqueConstraint("osm_id", name="buildings_unique_osm_id"),
)
