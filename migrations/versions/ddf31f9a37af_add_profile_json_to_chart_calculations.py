"""add_profile_json_to_chart_calculations

Revision ID: ddf31f9a37af
Revises: 9941e98f8708
Create Date: 2026-06-14 10:03:22.288273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddf31f9a37af'
down_revision: Union[str, Sequence[str], None] = '9941e98f8708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "chart_calculations",
        sa.Column(
            "profile_json",
            sa.JSON(),
            nullable=True
        )
    )


def downgrade():

    op.drop_column(
        "chart_calculations",
        "profile_json"
    )
