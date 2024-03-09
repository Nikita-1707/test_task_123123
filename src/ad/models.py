from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DateTime,
)
from sqlalchemy.dialects.postgresql import ENUM

from ad.schemas import AdTypeEnum
from auth.models import User
from database import metadata


ad_type_enum = ENUM(
    AdTypeEnum,
    name='ad_type_enum',
    create_type=False,
)


ad_table = Table(
    'ad',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', JSON),
    Column('type', ad_type_enum),
    Column('author_id', ForeignKey(User.id)),
)


comment_table = Table(
    'comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('author_id', ForeignKey(User.id)),
    Column('ad_id', ForeignKey(ad_table.c.id)),
)
