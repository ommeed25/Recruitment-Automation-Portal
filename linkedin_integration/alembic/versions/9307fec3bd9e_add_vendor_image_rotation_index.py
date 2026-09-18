from alembic import op
import sqlalchemy as sa


revision = "9307fec3bd9e"
down_revision = "b4d3612ccf96"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "vendor_settings",
        sa.Column(
            "rotation_index",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade():
    op.drop_column(
        "vendor_settings",
        "rotation_index",
        )
