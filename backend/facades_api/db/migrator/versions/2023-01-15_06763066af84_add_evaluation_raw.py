"""add_evaluation_raw

Revision ID: 06763066af84
Revises: 08e81fde0f66
Create Date: 2023-01-15 16:21:38.383192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "06763066af84"
down_revision = "08e81fde0f66"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("buildings", sa.Column("evaluation_raw", sa.Float(), server_default=sa.text("null"), nullable=True))
    op.alter_column("buildings", "evaluation", type_=sa.Numeric(precision=5, scale=3))
    op.execute("UPDATE buildings SET evaluation = 10.000 WHERE evaluation = 9.999")


def downgrade():
    op.drop_column("buildings", "evaluation_raw")
    op.execute("UPDATE buildings SET evaluation = 9.999 WHERE evaluation >= 10.0")
    op.alter_column("buildings", "evaluation", type_=sa.Numeric(precision=4, scale=3))
