from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import get_db, engine
from app.models import Base

app = FastAPI(title="AI Eval Platform")


# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    value = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "result": value}
