"""create vehicles

Revision ID: 20260712_0002
Revises: 20260712_0001
Create Date: 2026-07-12 00:15:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260712_0002"
down_revision = "20260712_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("registration_number", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=120), nullable=False),
        sa.Column("vehicle_type", sa.String(length=50), nullable=False),
        sa.Column("max_load_capacity", sa.Float(), nullable=False),
        sa.Column("odometer", sa.Float(), nullable=False, server_default="0"),
        sa.Column("acquisition_cost", sa.Float(), nullable=False, server_default="0"),
        sa.Column(
            "status",
            sa.Enum("Available", "On Trip", "In Shop", "Retired", name="vehicle_status", native_enum=False),
            nullable=False,
            server_default="Available",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("registration_number"),
    )
    op.create_index(op.f("ix_vehicles_registration_number"), "vehicles", ["registration_number"], unique=False)
    op.create_index(op.f("ix_vehicles_status"), "vehicles", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vehicles_status"), table_name="vehicles")
    op.drop_index(op.f("ix_vehicles_registration_number"), table_name="vehicles")
    op.drop_table("vehicles")
