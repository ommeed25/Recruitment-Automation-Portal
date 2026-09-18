"""Create Sales LinkedIn accounts table.

Revision ID: 4f6a8b1c2d3e
Revises: 9307fec3bd9e
Create Date: 2026-09-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f6a8b1c2d3e"
down_revision: Union[str, Sequence[str], None] = "9307fec3bd9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the Sales LinkedIn accounts table."""
    op.create_table(
        "sales_linkedin_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("linkedin_sub", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("token_type", sa.String(length=20), nullable=True),
        sa.Column("expires_in", sa.Integer(), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("linkedin_sub"),
    )
    op.create_index(
        op.f("ix_sales_linkedin_accounts_id"),
        "sales_linkedin_accounts",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the Sales LinkedIn accounts table."""
    op.drop_table("sales_linkedin_accounts")
