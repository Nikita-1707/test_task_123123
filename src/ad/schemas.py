from enum import Enum

from pydantic.main import BaseModel


class AdTypeEnum(str, Enum):
    sale = 'sale'
    missing = 'missing'


class AdCreate(BaseModel):
    title: str
    description: str
    type: AdTypeEnum


class AdRead(BaseModel):
    id: int
    title: str
    description: str


class ReportCreate(BaseModel):
    message: str
    ad_id: int


class ReportRead(BaseModel):
    id: int
    message: str
    ad_id: int
    reporter_id: int
