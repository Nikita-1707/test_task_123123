from enum import Enum

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


class AdFieldsForSorting(str, Enum):
    id = 'id'
    title = 'title'
    type = 'type'


report_table = Table(
    'report',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('message', String, nullable=False),
    Column('reporter_id', ForeignKey(User.id)),
    Column('ad_id', ForeignKey(ad_table.c.id, ondelete='CASCADE')),
)


class ReportFieldsForSorting(str, Enum):
    id = 'id'
    message = 'message'
    reporter_id = 'reporter_id'
