"""initial

Revision ID: 381c8c542364
Revises: 
Create Date: 2022-12-21 12:29:42.118244

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2

from facades_api.db.entities.buildings import buildings_id_seq
from facades_api.db.entities.deffect_types import deffect_types_id_seq
from facades_api.db.entities.deffects import deffects_id_seq
from facades_api.db.entities.mark_feedback import mark_feedback_id_seq
from facades_api.db.entities.marks import marks_id_seq
from facades_api.db.entities.photos import photos_id_seq
from facades_api.db.entities.users import users_id_seq
from facades_api.db.entities.users_auth import users_auth_id_seq

# revision identifiers, used by Alembic.
revision = "381c8c542364"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.execute(sa.schema.CreateSequence(buildings_id_seq))
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('buildings_id_seq')"), nullable=False),
        sa.Column("osm_id", sa.String(length=20), nullable=True),
        sa.Column("address", sa.String(length=256), nullable=True),
        sa.Column("building_year", sa.Integer(), nullable=True),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("buildings_pk")),
        sa.UniqueConstraint("osm_id", name="buildings_unique_osm_id"),
    )

    op.execute(sa.schema.CreateSequence(deffect_types_id_seq))
    op.create_table(
        "deffect_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('deffect_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("deffect_types_pk")),
        sa.UniqueConstraint("name", name="deffect_types_unique_name"),
    )

    op.execute(sa.schema.CreateSequence(users_id_seq))
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('users_id_seq')"), nullable=False),
        sa.Column("email", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=False),
        sa.Column("password_hash", sa.CHAR(length=128), nullable=False),
        sa.Column("registered_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pk")),
        sa.UniqueConstraint("email", name="users_unique_email"),
        sa.UniqueConstraint("name", name="users_unique_name"),
    )

    op.execute(sa.schema.CreateSequence(photos_id_seq))
    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('photos_id_seq')"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.Column(
            "type_id", sa.Enum("DEFFECT", "CLOSE_RANGE", "MIDDLE_RANGE", "WIDE_RANGE", name="ptenum"), nullable=True
        ),
        sa.Column(
            "point",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("loaded_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["building_id"],
            ["buildings.id"],
            name=op.f("photos_fk_building_id__buildings"),
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("photos_fk_user_id__users"), onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("photos_pk")),
    )

    op.execute(sa.schema.CreateSequence(users_auth_id_seq))
    op.create_table(
        "users_auth",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('users_auth_id_seq')"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("device", sa.String(length=200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("last_update", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("users_auth_fk_user_id__users")),
        sa.PrimaryKeyConstraint("id", name=op.f("users_auth_pk")),
    )

    op.execute(sa.schema.CreateSequence(marks_id_seq))
    op.create_table(
        "marks",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('marks_id_seq')"), nullable=False),
        sa.Column("photo_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("added_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("complaints", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["marks.id"], name=op.f("marks_fk_parent_id__marks")),
        sa.ForeignKeyConstraint(["photo_id"], ["photos.id"], name=op.f("marks_fk_photo_id__photos")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("marks_fk_user_id__users")),
        sa.PrimaryKeyConstraint("id", name=op.f("marks_pk")),
        sa.UniqueConstraint("photo_id", "user_id", "parent_id", name="marks_unique_photo_id_user_id"),
    )

    op.execute(sa.schema.CreateSequence(deffects_id_seq))
    op.create_table(
        "deffects",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('deffects_id_seq')"), nullable=False),
        sa.Column("mark_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("width", sa.Float(), nullable=False),
        sa.Column("height", sa.Float(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], name=op.f("deffects_fk_author_id__users")),
        sa.ForeignKeyConstraint(["mark_id"], ["marks.id"], name=op.f("deffects_fk_mark_id__marks")),
        sa.ForeignKeyConstraint(["type_id"], ["deffect_types.id"], name=op.f("deffects_fk_type_id__deffect_types")),
        sa.PrimaryKeyConstraint("id", name=op.f("deffects_pk")),
    )

    op.execute(sa.schema.CreateSequence(mark_feedback_id_seq))
    op.create_table(
        "mark_feedback",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('mark_feedback_id_seq')"), nullable=False),
        sa.Column("mark_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("feedback", sa.Enum("POSITIVE", "NEGATIVE", "COMPLAINT", name="mfenum"), nullable=False),
        sa.Column("left_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["mark_id"], ["marks.id"], name=op.f("mark_feedback_fk_mark_id__marks")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("mark_feedback_fk_user_id__users")),
        sa.PrimaryKeyConstraint("id", name=op.f("mark_feedback_pk")),
        sa.UniqueConstraint("mark_id", "user_id", name="mark_feedback_unique_mark_id_user_id"),
    )


def downgrade():
    op.drop_table("mark_feedback")
    op.drop_table("deffects")
    op.drop_table("marks")
    op.drop_table("users_auth")
    op.drop_table("photos")
    op.drop_table("users")
    op.drop_table("deffect_types")
    op.drop_table("buildings")
    sa.schema.DropSequence(mark_feedback_id_seq)
    sa.schema.DropSequence(deffects_id_seq)
    sa.schema.DropSequence(marks_id_seq)
    sa.schema.DropSequence(users_auth_id_seq)
    sa.schema.DropSequence(photos_id_seq)
    sa.schema.DropSequence(users_id_seq)
    sa.schema.DropSequence(deffect_types_id_seq)
    sa.schema.DropSequence(buildings_id_seq)
