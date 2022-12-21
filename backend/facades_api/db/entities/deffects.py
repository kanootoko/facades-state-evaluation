# pylint: disable=too-many-ancestors, abstract-method
"""
Deffects database table is defined here.
"""
from typing import NamedTuple

from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, Table

from facades_api.db import metadata


class DeffectsTable(Table):
    """
    An attempt to annotate deffects columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "DeffectsColumns",
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


deffects_id_seq = Sequence("deffects_id_seq")


deffects = DeffectsTable(
    "deffects",
    metadata,
    Column("id", Integer, deffects_id_seq, server_default=deffects_id_seq.next_value(), primary_key=True),
    Column("mark_id", Integer, ForeignKey("marks.id"), nullable=False),
    Column("author_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("x", Float, nullable=False),
    Column("y", Float, nullable=False),
    Column("width", Float, nullable=False),
    Column("height", Float, nullable=False),
    Column("type_id", Integer, ForeignKey("deffect_types.id"), nullable=False),
)
