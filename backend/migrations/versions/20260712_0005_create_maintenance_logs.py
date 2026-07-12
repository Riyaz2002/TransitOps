"""create maintenance logs

Revision ID: 20260712_0005
Revises: 20260712_0004
Create Date: 2026-07-12 01:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260712_0005"
down_revision = "20260712_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "maintenance_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("vehicle_id", sa.Integer(), nullable=False),
        sa.Column(
            "maintenance_type",
            sa.Enum("Oil Change", "Tire Replacement", "Brake Service", "Engine Repair", "Transmission Repair", "Electrical Repair", "Inspection", "Other", name="maintenance_type", native_enum=False),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("cost", sa.Float(), nullable=False, server_default="0"),
        sa.Column(
            "status",
            sa.Enum("Open", "Closed", name="maintenance_status", native_enum=False),
            nullable=False,
            server_default="Open",
        ),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["vehicle_id"], ["vehicles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_maintenance_logs_vehicle_id"), "maintenance_logs", ["vehicle_id"], unique=False)
    op.create_index(op.f("ix_maintenance_logs_status"), "maintenance_logs", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_maintenance_logs_status"), table_name="maintenance_logs")
    op.drop_index(op.f("ix_maintenance_logs_vehicle_id"), table_name="maintenance_logs")
    op.drop_table("maintenance_logs")
