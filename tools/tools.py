import asyncio
import datetime
import os
import uuid
from typing import Final

import httpx
from sqlalchemy.orm import Session

from app import models
from dto.dtos import ArticleDto
from tools.logs import get_logger

logger = get_logger()

CREATE_ARTICLE_ENDPOINT: Final[str] = "/articles"
DEFAULT_GO_SERVER: Final[str] = "http://localhost:8000"

http_client: httpx.AsyncClient | None = None


async def init_http_client() -> None:
    global http_client
    if http_client is None:
        http_client = httpx.AsyncClient(
            http2=True,
            timeout=15.0,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=50,
                keepalive_expiry=60.0,
            ),
        )


async def close_http_client() -> None:
    global http_client
    if http_client is not None:
        await http_client.aclose()
        http_client = None


async def create_article(index: int, session: Session) -> None:
    if http_client is None:
        raise RuntimeError("HTTP client not initialized")

    article = ArticleDto(
        pub_date=datetime.datetime.now(datetime.UTC).isoformat(),
        headline=str(uuid.uuid4()),
        content=str(uuid.uuid4()),
    )

    url = f"{os.getenv('GO_SERVER', DEFAULT_GO_SERVER).rstrip('/')}{CREATE_ARTICLE_ENDPOINT}"
    headers = {"Content-Type": "application/json"}

    try:
        response = await http_client.post(
            url,
            json=article.model_dump(mode="json"),
            headers=headers,
        )
        response.raise_for_status()

        if response.status_code != 200:
            logger.warning(f"Unexpected status {response.status_code} for article {index}")
            return

        data = response.json()
        external_id = data.get("external_id")

        if not external_id:
            logger.error(f"No external_id returned for article {index}")
            return

        db_article = models.Article(**article.model_dump())
        session.add(db_article)
        session.flush()

        session.add(
            models.ExternalId(
                external_id=external_id,
                article_id=db_article.id,
            )
        )
        session.commit()

    except httpx.RequestError as e:
        logger.error(f"Network error article {index}: {e.__class__.__name__} {e}")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error {e.response.status_code} article {index}: {e.response.text[:200]}")
    except Exception as e:
        logger.exception(f"Unexpected error article {index}")
        session.rollback()


async def generate_articles(count: int, session: Session) -> None:
    semaphore = asyncio.Semaphore(20)

    async def bounded_create(i: int) -> None:
        async with semaphore:
            await create_article(i, session)

    tasks = [asyncio.create_task(bounded_create(i)) for i in range(count)]
    await asyncio.gather(*tasks, return_exceptions=True)
