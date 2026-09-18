"""Create Sales settings table

Revision ID: b23703905ea9
Revises: 7722bd33a70e
Create Date: 2026-09-18 15:49:42.355476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b23703905ea9'
down_revision: Union[str, Sequence[str], None] = '7722bd33a70e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sales_settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_enabled", sa.Boolean(), nullable=False),
        sa.Column("posting_time", sa.String(length=10), nullable=False),
        sa.Column("active_image_id", sa.Integer(), nullable=True),
        sa.Column("rotation_index", sa.Integer(), nullable=False),
        sa.Column("last_rotation_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["active_image_id"],
            ["sales_images.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_sales_settings_id"),
        "sales_settings",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_sales_settings_id"),
        table_name="sales_settings",
    )
    op.drop_table("sales_settings")
