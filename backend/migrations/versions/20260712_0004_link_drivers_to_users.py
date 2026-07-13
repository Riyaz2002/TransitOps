"""link drivers to users

Revision ID: 20260712_0004
Revises: 20260712_0003
Create Date: 2026-07-12 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "20260712_0004"
down_revision = "20260712_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("drivers", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_drivers_user_id_users", "drivers", "users", ["user_id"], ["id"], ondelete="SET NULL")
    op.create_unique_constraint("uq_drivers_user_id", "drivers", ["user_id"])


def downgrade() -> None:
    op.drop_constraint("uq_drivers_user_id", "drivers", type_="unique")
    op.drop_constraint("fk_drivers_user_id_users", "drivers", type_="foreignkey")
    op.drop_column("drivers", "user_id")
