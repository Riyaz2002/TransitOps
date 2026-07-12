"""create drivers

Revision ID: 20260712_0004
Revises: 20260712_0003
Create Date: 2026-07-12 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260712_0004"
down_revision = "20260712_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("license_number", sa.String(length=50), nullable=False),
        sa.Column("license_category", sa.String(length=50), nullable=False),
        sa.Column("license_expiry_date", sa.Date(), nullable=False),
        sa.Column("contact_number", sa.String(length=30), nullable=False),
        sa.Column("safety_score", sa.Float(), nullable=False, server_default="100"),
        sa.Column("status", sa.Enum("Available", "On Trip", "Off Duty", "Suspended", name="driver_status", native_enum=False), nullable=False, server_default="Available"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("license_number"),
    )
    op.create_index(op.f("ix_drivers_license_number"), "drivers", ["license_number"], unique=False)
    op.create_index(op.f("ix_drivers_license_expiry_date"), "drivers", ["license_expiry_date"], unique=False)
    op.create_index(op.f("ix_drivers_status"), "drivers", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_drivers_status"), table_name="drivers")
    op.drop_index(op.f("ix_drivers_license_expiry_date"), table_name="drivers")
    op.drop_index(op.f("ix_drivers_license_number"), table_name="drivers")
    op.drop_table("drivers")
