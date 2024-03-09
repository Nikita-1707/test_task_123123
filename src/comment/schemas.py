import datetime

from pydantic.main import BaseModel


class CommentCreate(BaseModel):
    text: str
    ad_id: int


class CommentRead(BaseModel):
    id: int
    text: str
    created_at: datetime.datetime
    author_email: str
