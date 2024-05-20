import asyncio
import datetime
import logging
import os
import uuid
from asyncio import AbstractEventLoop

import aiohttp

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def create_article(loop: AbstractEventLoop) -> dict | None:
    """
    Create an article on the go-server
    :param loop: current event loop
    :return: article identifier at the go-server
    """
    pub_date = datetime.datetime.now()
    data = {
        "pub_date": str(pub_date), "headline": str(uuid.uuid4()), "content": str(uuid.uuid4())
    }
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.post(url=os.getenv("GO_SERVER", 'http://localhost:8000'), json=data,
                                headers=headers) as resp:
            if resp.status == 201:
                logger.debug(f"Created article with content {data} \n status code {resp.status}")
                logger.debug(f"answer was {await resp.json()}")
                return await resp.json()
            if resp.status == 400:
                logger.debug(await resp.text())
    return None


async def generate_articles(num: int) -> list[dict | None]:
    """
        Task which generates articles and post them to go server
    :param num: number of articles which will be generated
    :return: created tasks
    """
    loop = asyncio.get_event_loop()
    tasks = [await create_article(loop) for _ in range(num)]
    logger.debug(tasks)
    return tasks
