# pylint: disable=too-many-ancestors, abstract-method
"""
Defect Types database table is defined here.
"""
from typing import NamedTuple

from sqlalchemy import Column, Integer, Sequence, String, Table, UniqueConstraint

from facades_api.db import metadata


class DefectTypesTable(Table):
    """
    An attempt to annotate defect_types columns.
    """

    __annotations__ = Table.__annotations__ | {
        "c": NamedTuple(
            "DefectTypesColumns",
            [
                ("id", int),
                ("name", str),
            ],
        )
    }


defect_types_id_seq = Sequence("defect_types_id_seq")

defect_types = DefectTypesTable(
    "defect_types",
    metadata,
    Column("id", Integer, defect_types_id_seq, server_default=defect_types_id_seq.next_value(), primary_key=True),
    Column("name", String(40), nullable=False),
    UniqueConstraint("name", name="defect_types_unique_name"),
)
