from sqlalchemy import (
    JSON,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
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
