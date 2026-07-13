"""add drivers

Revision ID: 20260712_0003
Revises: 20260712_0002
Create Date: 2026-07-12 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260712_0003"
down_revision = "20260712_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("license_number", sa.String(length=80), nullable=False),
        sa.Column("license_category", sa.String(length=50), nullable=False),
        sa.Column("license_expiry_date", sa.Date(), nullable=False),
        sa.Column("contact_number", sa.String(length=20), nullable=False),
        sa.Column("safety_score", sa.Numeric(precision=5, scale=2), nullable=False, server_default="100"),
        sa.Column(
            "status",
            sa.Enum("available", "on_trip", "off_duty", "suspended", name="driver_status", native_enum=False),
            nullable=False,
            server_default="available",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("license_number"),
    )
    op.create_index(op.f("ix_drivers_license_number"), "drivers", ["license_number"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_drivers_license_number"), table_name="drivers")
    op.drop_table("drivers")
