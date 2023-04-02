# pylint: disable=too-many-ancestors, abstract-method
"""
Defects database table is defined here.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, Table

from facades_api.db import metadata


defects_id_seq = Sequence("defects_id_seq")

defects = Table(
    "defects",
    metadata,
    Column("id", Integer, defects_id_seq, server_default=defects_id_seq.next_value(), primary_key=True),
    Column("mark_id", Integer, ForeignKey("marks.id"), nullable=False),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("x", Float, nullable=False),
    Column("y", Float, nullable=False),
    Column("width", Float, nullable=False),
    Column("height", Float, nullable=False),
    Column("type_id", Integer, ForeignKey("defect_types.id"), nullable=False),
)
"""
Facades defects.

Columns:
- `id` - defect identifier, int serial
- `mark_id` - mark (deffects group) identifier, int
- `author_id` - identifier of the user who marked the deffect, int
- `x` - horizontal relative coordinate of start of a deffect on a photo, from 0.0 to 1.0, float
- `y` - vertical relative coordinate of startof a deffect on a photo, from 0.0 to 1.0, float
- `width` - horizontal relative length of a deffect on a photo, from 0.0 to 1.0, float
- `y` - verticalrelative length of a deffect on a photo, from 0.0 to 1.0, float
- `type_id` - feccrect type identifier, int
"""
