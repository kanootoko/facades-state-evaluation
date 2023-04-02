# pylint: disable=too-many-ancestors, abstract-method
"""
Defect Types database table is defined here.
"""
from sqlalchemy import Column, Integer, Sequence, String, Table, UniqueConstraint

from facades_api.db import metadata


defect_types_id_seq = Sequence("defect_types_id_seq")

defect_types = Table(
    "defect_types",
    metadata,
    Column("id", Integer, defect_types_id_seq, server_default=defect_types_id_seq.next_value(), primary_key=True),
    Column("name", String(40), nullable=False),
    UniqueConstraint("name", name="defect_types_unique_name"),
)
"""
Facades defect types.

Columns:
- `id` - defect types identifier, int serial
- `name` - name of facade defect, varchar(40)
"""
