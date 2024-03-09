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
