from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.db import get_db, engine
from app.models import Base
from app.routers import test_suites, prompts, experiments, comparisons, leaderboard


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


# ✅ CORS CONFIGURATION
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(test_suites.router)
app.include_router(prompts.router)
app.include_router(experiments.router)
app.include_router(comparisons.router)
app.include_router(leaderboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    value = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "result": value}