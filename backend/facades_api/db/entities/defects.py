# pylint: disable=too-many-ancestors, abstract-method
"""
Defects database table is defined here.
"""
from typing import NamedTuple

from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, Table

from facades_api.db import metadata


class DefectsTable(Table):
    """
    An attempt to annotate defects columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "DefectsColumns",
            [
                ("id", int),
                ("mark_id", int),
                ("author_id", int),
                ("x", float),
                ("y", float),
                ("width", float),
                ("height", float),
                ("type_id", int),
            ],
        )
    }


defects_id_seq = Sequence("defects_id_seq")


defects = DefectsTable(
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
