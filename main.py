import datetime
import logging
import uuid
from asyncio import AbstractEventLoop

import aiohttp
import asyncio

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def create_article(loop: AbstractEventLoop):
    pub_date = datetime.datetime.now()
    data = {
        "pub_date": str(pub_date), "headline": str(uuid.uuid4()), "content": str(uuid.uuid4())
    }
    headers = {"Content-Type": "application/json"}
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.post(url='http://localhost:8000', json=data, headers=headers) as resp:
            if resp.status == 201:
                logger.debug(f"Created article with content {data} \n status code {resp.status}")
                logger.debug(f"answer was {await resp.json()}")
            if resp.status == 400:
                logger.debug(await resp.text())


async def main():
    loop = asyncio.get_event_loop()
    tasks = [await create_article(loop) for _ in range(100)]
    logger.debug(tasks)

if __name__ == '__main__':
    asyncio.run(main())
