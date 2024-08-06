import datetime

from pydantic import BaseModel


class ArticleDto(BaseModel):
    pub_date: str
    headline: str
    content: str
