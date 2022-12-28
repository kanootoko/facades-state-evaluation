# pylint: disable=too-many-ancestors, abstract-method
"""
Photos database table is defined here.
"""
from datetime import datetime
from typing import NamedTuple

from geoalchemy2 import Geometry
from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Sequence, Table

from facades_api.db import metadata
from facades_api.db.entities.enums import PTEnum


class PhotosTable(Table):
    """
    An attempt to annotate photos columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "PhotosColumns",
            [
                ("id", int),
                ("user_id", int),
                ("building_id", int),
                ("angle_type", int),
                ("point", Geometry),
                ("loaded_at", datetime),
            ],
        )
    }


photos_id_seq = Sequence("photos_id_seq")


photos = PhotosTable(
    "photos",
    metadata,
    Column("id", Integer, photos_id_seq, server_default=photos_id_seq.next_value(), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("building_id", Integer, ForeignKey("buildings.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("angle_type", Enum(PTEnum), nullable=True),
    Column("point", Geometry("POINT", srid=4326)),
    Column("loaded_at", TIMESTAMP(timezone=True)),
)
