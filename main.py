import uvicorn
from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import users, items, runs

models.Base.metadata.create_all(bind=engine)


def get_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(users.router)
    _app.include_router(items.router)
    _app.include_router(runs.router)
    return _app


app = get_app()


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8001)
