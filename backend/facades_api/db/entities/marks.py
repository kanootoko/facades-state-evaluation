# pylint: disable=too-many-ancestors, abstract-method
"""
Marks database table is defined here.
"""
from datetime import datetime
from typing import NamedTuple

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Sequence, Table, UniqueConstraint, func

from facades_api.db import metadata


class MarksTable(Table):
    """
    An attempt to annotate marks columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "MarksColumns",
            [
                ("id", int),
                ("photo_id", int),
                ("user_id", int),
                ("parent_id", int),
                ("added_at", datetime),
                ("rating", int),
                ("complaints", int),
            ],
        )
    }


marks_id_seq = Sequence("marks_id_seq")


marks = MarksTable(
    "marks",
    metadata,
    Column("id", Integer, marks_id_seq, server_default=marks_id_seq.next_value(), primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("parent_id", Integer, ForeignKey("marks.id")),
    Column("added_at", TIMESTAMP(timezone=True), nullable=False, default=func.now()),
    Column("rating", Integer, nullable=False, default=0),
    Column("complaints", Integer, nullable=False, default=0),
    UniqueConstraint("photo_id", "user_id", "parent_id", name="marks_unique_photo_id_user_id"),
)
