"""rename defect

Revision ID: 08e81fde0f66
Revises: d8a0067c3f5f
Create Date: 2023-01-14 22:13:56.236133

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '08e81fde0f66'
down_revision = 'd8a0067c3f5f'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("deffects", "defects")
    op.rename_table("deffect_types", "defect_types")
    op.execute("ALTER TYPE ptenum RENAME VALUE 'DEFFECT' to 'DEFECT'")
    op.execute("ALTER INDEX deffect_types_unique_name RENAME TO defect_types_unique_name")
    op.execute("ALTER INDEX deffects_pk RENAME TO defects_pk")
    op.execute("ALTER INDEX deffect_types_pk RENAME TO defect_types_pk")
    op.execute("ALTER SEQUENCE deffect_types_id_seq RENAME TO defect_types_id_seq")
    op.execute("ALTER SEQUENCE deffects_id_seq RENAME TO defects_id_seq")
    op.execute("ALTER TABLE defects RENAME CONSTRAINT deffects_fk_author_id__users TO defects_fk_author_id__users")
    op.execute("ALTER TABLE defects RENAME CONSTRAINT deffects_fk_mark_id__marks TO defects_fk_mark_id__marks")
    op.execute("ALTER TABLE defects RENAME CONSTRAINT deffects_fk_type_id__deffect_types TO defects_fk_type_id__deffect_types")


def downgrade():
    op.rename_table("defects", "deffects")
    op.rename_table("defect_types", "deffect_types")
    op.execute("ALTER TYPE ptenum RENAME VALUE 'DEFECT' to 'DEFFECT'")
    op.execute("ALTER INDEX defect_types_unique_name RENAME TO deffect_types_unique_name")
    op.execute("ALTER INDEX defects_pk RENAME TO deffects_pk")
    op.execute("ALTER INDEX defect_types_pk RENAME TO deffect_types_pk")
    op.execute("ALTER SEQUENCE defect_types_id_seq RENAME TO deffect_types_id_seq")
    op.execute("ALTER SEQUENCE defects_id_seq RENAME TO deffects_id_seq")
    op.execute("ALTER TABLE deffects RENAME CONSTRAINT defects_fk_author_id__users TO deffects_fk_author_id__users")
    op.execute("ALTER TABLE deffects RENAME CONSTRAINT defects_fk_mark_id__marks TO deffects_fk_mark_id__marks")
    op.execute("ALTER TABLE deffects RENAME CONSTRAINT defects_fk_type_id__deffect_types TO deffects_fk_type_id__deffect_types")
