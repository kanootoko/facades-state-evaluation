# pylint: disable=too-many-ancestors, abstract-method
"""
Marks database table is defined here.
"""
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Sequence, Table, UniqueConstraint, func

from facades_api.db import metadata


marks_id_seq = Sequence("marks_id_seq")

marks = Table(
    "marks",
    metadata,
    Column("id", Integer, marks_id_seq, server_default=marks_id_seq.next_value(), primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("parent_id", Integer, ForeignKey("marks.id")),
    Column(
        "added_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()  # pylint: disable=not-callable
    ),
    Column("rating", Integer, nullable=False, default=0),
    Column("complaints", Integer, nullable=False, default=0),
    UniqueConstraint("photo_id", "user_id", "parent_id", name="marks_unique_photo_id_user_id"),
)
"""
Marks (groups of defects).

Columns:
- `id` - mark identifier, int serial
- `photo_id` - photo identifier, int
- `user_id` - identifier of the user who created the mark, int
- `parent_id` - identifier of a mark used as starting point in marking, int
- `added_at` - datetime of a mark creation, timestamptz
- `rating` - sum of feedbacks left by other users, int
- `complaints` - number of complaints left by other user on a mark, int
"""
