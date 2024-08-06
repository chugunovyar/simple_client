from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from tools.logs import get_logger
from tools.tools import generate_articles

router = APIRouter()
logger = get_logger()


@router.get("/run/")
async def runner(request: Request, _runner: schemas.Run, background_tasks: BackgroundTasks,
                 db: Session = Depends(get_db)):
    logger.debug(f"{_runner}")
    logger.debug(request)
    background_tasks.add_task(generate_articles, _runner.num, db)
    return {"message": "Running"}
