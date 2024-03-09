from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
)

from ad.models import ad_table
from auth.models import User
from database import metadata

comment_table = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('author_id', ForeignKey(User.id)),
    Column('ad_id', ForeignKey(ad_table.c.id, ondelete='CASCADE')),
)
