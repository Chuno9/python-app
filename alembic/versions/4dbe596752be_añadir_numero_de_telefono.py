"""añadir numero de telefono

Revision ID: 4dbe596752be
Revises: 
Create Date: 2026-03-11 08:21:30.469483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dbe596752be'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("usuarios", sa.Column("tel", sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("usuarios", "tel")
