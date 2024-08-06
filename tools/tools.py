import asyncio
import datetime
import os
import uuid

import httpx
from sqlalchemy.orm import Session

from app import models
from dto.dtos import ArticleDto
from tools.logs import get_logger

logger = get_logger()


async def create_article(_i: int, db: Session):
    article = ArticleDto(pub_date=str(datetime.datetime.now()),
                         headline=str(uuid.uuid4()), content=str(uuid.uuid4()))
    headers = {"Content-Type": "application/json"}
    url = os.getenv('GO_SERVER', 'http://localhost:8000')
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=article.dict(), headers=headers)
        logger.debug(f"{response.status_code} {_i} {article.json()}")
        if response.status_code == 201:
            _resp: dict = response.json()
            articles = models.Article(**article.dict())
            db.add(articles)
            db.commit()

            ext_db = models.ExternalId(external_id=_resp['external_id'], article_id=articles.id)
            db.add(ext_db)
            db.commit()


async def generate_articles(num: int, db: Session):
    for i in range(num):
        logger.debug(f"Generating {i}")
        asyncio.create_task(create_article(i, db))
