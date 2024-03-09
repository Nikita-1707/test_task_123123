"""Add roles

Revision ID: e4783e8ba21b
Revises: 
Create Date: 2024-03-08 13:39:11.240642

"""
from alembic import op

from auth.models import client_role

# revision identifiers, used by Alembic.
revision = 'e4783e8ba21b'
down_revision = 'e4783e8ba21a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(
        table=client_role,
        rows=[
            {
                'id': 1,
                'name': 'user',
                'permissions': {},
            },
            {
                'id': 2,
                'name': 'admin',
                'permissions': {},
            },
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
