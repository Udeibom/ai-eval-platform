from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.db import get_db, engine
from app.models import Base
from app.routers import test_suites, prompts


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    print("Tables created")

    yield

    # Shutdown logic (optional)
    print("Application shutdown")


app = FastAPI(
    title="AI Eval Platform",
    lifespan=lifespan
)


# Include routers
app.include_router(test_suites.router)
app.include_router(prompts.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    value = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "result": value}
