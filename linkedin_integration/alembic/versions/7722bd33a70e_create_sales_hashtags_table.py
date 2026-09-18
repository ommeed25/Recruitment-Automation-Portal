"""Create Sales hashtags table

Revision ID: 7722bd33a70e
Revises: 4f32fb8d146f
Create Date: 2026-09-18 15:30:30.839933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7722bd33a70e'
down_revision: Union[str, Sequence[str], None] = '4f32fb8d146f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "sales_hashtags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hashtag", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
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
    )

    op.create_index(
        op.f("ix_sales_hashtags_id"),
        "sales_hashtags",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_sales_hashtags_id"),
        table_name="sales_hashtags",
    )
    op.drop_table("sales_hashtags")
