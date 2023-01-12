"""refresh_tokens  
... by adding refresh_until to users_auth  
Add refresh tokens support to users_auth  
Rename photos.type_id -> angle_type  
Rename users_auth.last_update -> valid_until  
Add indexes to users_auth table: (device and user_id) and (user_id and device)
Add index to users table: email

Revision ID: 223ce64b8794
Revises: 381c8c542364
Create Date: 2023-01-13 21:39:56.579133

"""
import sqlalchemy as sa
from alembic import op

from facades_api.db.entities import deffect_types

# revision identifiers, used by Alembic.
revision = "223ce64b8794"
down_revision = "381c8c542364"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("users_auth_unique_user_id_device", "users_auth", ["user_id", "device"])
    op.add_column("users_auth", sa.Column("refresh_until", sa.TIMESTAMP(timezone=True), nullable=False))

    op.alter_column("photos", "type_id", new_column_name="angle_type")
    op.alter_column("users_auth", "last_update", new_column_name="valid_until")

    op.alter_column("mark_feedback", "left_at", server_default=sa.func.now())
    op.alter_column("marks", "added_at", server_default=sa.func.now())
    op.alter_column("photos", "loaded_at", server_default=sa.func.now())
    op.alter_column("users", "registered_at", server_default=sa.func.now())
    op.create_index("users_auth_index_device_user_id", "users_auth", ["device", "user_id"])
    op.create_index("users_auth_index_user_id_device", "users_auth", ["user_id", "device"])
    op.create_index("users_index_email", "users", ["email"])

    op.bulk_insert(
        deffect_types,
        [
            {"name": "bricks"},
            {"name": "wall_damage"},
            {"name": "crack"},
            {"name": "construction"},
        ],
    )


def downgrade():
    op.drop_index("users_index_email")
    op.drop_index("users_auth_index_user_id_device")
    op.drop_index("users_auth_index_device_user_id")
    op.alter_column("users", "registered_at", server_default=None)
    op.alter_column("photos", "loaded_at", server_default=None)
    op.alter_column("marks", "added_at", server_default=None)
    op.alter_column("mark_feedback", "left_at", server_default=None)

    op.alter_column("photos", "angle_type", new_column_name="type_id")
    op.alter_column("users_auth", "valid_until", new_column_name="last_update")

    op.drop_constraint("users_auth_unique_user_id_device", "users_auth", type_="unique")
    op.drop_column("users_auth", "refresh_until")

    op.execute("DELETE FROM deffect_types")
    op.execute("ALTER SEQUENCE deffect_types_id_seq RESTART WITH 1")