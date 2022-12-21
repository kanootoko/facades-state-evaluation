# pylint: disable=too-many-ancestors, abstract-method
"""
Deffect Types database table is defined here.
"""
from typing import NamedTuple

from sqlalchemy import Column, Integer, Sequence, String, Table, UniqueConstraint

from facades_api.db import metadata


class DeffectTypesTable(Table):
    """
    An attempt to annotate deffect_types columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "DeffectTypesColumns",
            [
                ("id", int),
                ("name", str),
            ],
        )
    }


deffect_types_id_seq = Sequence("deffect_types_id_seq")

deffect_types = DeffectTypesTable(
    "deffect_types",
    metadata,
    Column("id", Integer, deffect_types_id_seq, server_default=deffect_types_id_seq.next_value(), primary_key=True),
    Column("name", String(40), nullable=False),
    UniqueConstraint("name", name="deffect_types_unique_name"),
)
