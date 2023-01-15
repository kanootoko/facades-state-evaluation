"""add_robot
Add robot account with id 1
Add evaluation column to buildings

Revision ID: d8a0067c3f5f
Revises: 223ce64b8794
Create Date: 2023-01-13 05:29:30.846471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d8a0067c3f5f"
down_revision = "223ce64b8794"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "buildings",
        sa.Column("evaluation", sa.Numeric(precision=4, scale=3), nullable=True, server_default=sa.text("null")),
    )
    op.execute(
        "INSERT INTO users (id, name, email, password_hash, registered_at, is_active) VALUES (0, 'robot',"
        " 'robot@ai.com', 'no_hash_no_login', '2022-12-21 12:30', 'true')"
    )


def downgrade():
    op.execute("DELETE FROM users WHERE id = 0")
    op.drop_column("buildings", "evaluation")
