# pylint: disable=too-many-ancestors, abstract-method
"""
Mark Feedback database table is defined here.
"""
from datetime import datetime
from typing import NamedTuple

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer, Sequence, Table, UniqueConstraint, func

from facades_api.db import metadata
from facades_api.db.entities.enums import MFEnum


class MarkFeedbackTable(Table):
    """
    An attempt to annotate mark_feedback columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "MarkFeedbackColumns",
            [
                ("id", int),
                ("mark_id", int),
                ("user_id", int),
                ("feedback", MFEnum),
                ("left_at", datetime),
            ],
        )
    }


mark_feedback_id_seq = Sequence("mark_feedback_id_seq")

mark_feedback = MarkFeedbackTable(
    "mark_feedback",
    metadata,
    Column("id", Integer, mark_feedback_id_seq, server_default=mark_feedback_id_seq.next_value(), primary_key=True),
    Column("mark_id", Integer, ForeignKey("marks.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("feedback", Enum(MFEnum), nullable=False),
    Column("left_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    UniqueConstraint("mark_id", "user_id", name="mark_feedback_unique_mark_id_user_id"),
)
