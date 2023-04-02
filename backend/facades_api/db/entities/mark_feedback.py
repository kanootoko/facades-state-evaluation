# pylint: disable=too-many-ancestors, abstract-method
"""
Mark Feedback database table is defined here.
"""

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Sequence, Table, UniqueConstraint, func

from facades_api.db import metadata
from facades_api.db.entities.enums import MFEnum


mark_feedback_id_seq = Sequence("mark_feedback_id_seq")

mark_feedback = Table(
    "mark_feedback",
    metadata,
    Column("id", Integer, mark_feedback_id_seq, server_default=mark_feedback_id_seq.next_value(), primary_key=True),
    Column("mark_id", Integer, ForeignKey("marks.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("feedback", Enum(MFEnum), nullable=False),
    Column(
        "left_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()  # pylint: disable=not-callable
    ),
    UniqueConstraint("mark_id", "user_id", name="mark_feedback_unique_mark_id_user_id"),
)
"""
Mark feedbacks left by other users.

Columns:
- `id` - feedback identifier, int serial
- `mark_id` - mark (deffects group) identifier, int
- `user_id` - identifier of the user who left feedback, int
- `feedback` - feedback value left by user, MFEnum
- `left_at` - datetime of when feedback was last updated, timestamptz
"""
