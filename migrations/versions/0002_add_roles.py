"""Add roles

Revision ID: e4783e8ba21b
Revises: 
Create Date: 2024-03-08 13:39:11.240642

"""
from alembic import op

from auth.constants import user_role_id, admin_role_id
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
                'id': user_role_id,
                'name': 'user',
                'permissions': {},
            },
            {
                'id': admin_role_id,
                'name': 'admin',
                'permissions': {},
            },
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
