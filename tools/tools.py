import asyncio
import datetime
import os
import uuid

import httpx

from tools.logs import get_logger

logger = get_logger()


async def create_article(_i: int):
    """
    Create an article on the go-server
    :param _i:
    :return: article identifier at the go-server
    """
    pub_date = datetime.datetime.now()
    data = {
        "pub_date": str(pub_date), "headline": str(uuid.uuid4()), "content": str(uuid.uuid4())
    }
    headers = {"Content-Type": "application/json"}
    url = os.getenv('GO_SERVER', 'http://localhost:8000')
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
        logger.debug(f"{response.status_code} {_i}")


async def generate_articles(num: int):
    for i in range(num):
        logger.debug(f"Generating {i}")
        asyncio.create_task(create_article(i))
