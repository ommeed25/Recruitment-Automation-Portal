"""Create Sales post history table

Revision ID: 8af4eb089171
Revises: b23703905ea9
Create Date: 2026-09-18 15:58:35.131016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af4eb089171'
down_revision: Union[str, Sequence[str], None] = 'b23703905ea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "sales_post_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sales_linkedin_account_id", sa.Integer(), nullable=False),
        sa.Column("linkedin_post_id", sa.String(length=255), nullable=True),
        sa.Column("post_status", sa.String(length=50), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("posted_at", sa.TIMESTAMP(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["sales_linkedin_account_id"],
            ["sales_linkedin_accounts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_sales_post_history_id"),
        "sales_post_history",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_sales_post_history_id"),
        table_name="sales_post_history",
    )
    op.drop_table("sales_post_history")
