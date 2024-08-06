import asyncio
import uuid
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from app import models
from app.database import engine, SessionLocal
from app.routers import users, items, runs
from tools.tools import init_http_client, close_http_client, generate_articles

models.Base.metadata.create_all(bind=engine)

task_queue: asyncio.Queue = asyncio.Queue()
task_status: dict = {}


async def worker() -> None:
    while True:
        task_id, num = await task_queue.get()
        start = datetime.utcnow()
        task_status[task_id] = {
            "status": "running",
            "start": start.isoformat(),
            "num": num,
            "processed": 0,
        }

        try:
            db = next(SessionLocal())
            await generate_articles(num, db)
            end = datetime.utcnow()
            task_status[task_id].update({
                "status": "completed",
                "end": end.isoformat(),
                "duration_sec": (end - start).total_seconds(),
            })
        except Exception as e:
            task_status[task_id].update({
                "status": "failed",
                "error": str(e),
            })
        finally:
            task_queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_http_client()
    asyncio.create_task(worker())
    yield
    await close_http_client()


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(runs.router)


@app.post("/run/")
async def start_run(payload: dict = Body(...)):
    num = int(payload.get("num", 0))
    if num <= 0:
        return JSONResponse({"error": "num must be positive"}, status_code=400)

    task_id = str(uuid.uuid4())
    await task_queue.put((task_id, num))

    return {
        "status": "accepted",
        "task_id": task_id,
        "num": num,
        "check_status_url": f"/run/status/{task_id}",
    }


@app.get("/run/status/{task_id}")
async def get_status(task_id: str):
    info = task_status.get(task_id)
    if info is None:
        return JSONResponse({"error": "Task not found"}, status_code=404)
    return info


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        workers=1,
        limit_concurrency=200,
    )
