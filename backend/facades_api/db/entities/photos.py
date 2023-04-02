# pylint: disable=too-many-ancestors, abstract-method
"""
Photos database table is defined here.
"""
from geoalchemy2 import Geometry
from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Sequence, Table, func

from facades_api.db import metadata
from facades_api.db.entities.enums import PTEnum

photos_id_seq = Sequence("photos_id_seq")

photos = Table(
    "photos",
    metadata,
    Column("id", Integer, photos_id_seq, server_default=photos_id_seq.next_value(), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("building_id", Integer, ForeignKey("buildings.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("angle_type", Enum(PTEnum)),
    Column("point", Geometry("POINT", srid=4326)),
    Column("loaded_at", TIMESTAMP(timezone=True), server_default=func.now()),  # pylint: disable=not-callable
)
"""
Facades photos uploaded by users.

Columns:
- `id` - photo identifier, int serial
- `user_id` - identifier of the user who uploaded the photo, int
- `building_id` - building identifier, int
- `angle_type` - photo type in a context of view angle, PTEnum
- `point` - point from where photo was taken, Geometry, nullable
- `loaded_at` - datetime when photo was uploaded, timestamptz
"""
