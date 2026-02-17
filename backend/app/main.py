from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db

app = FastAPI(title="AI Eval Platform")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    value = db.execute(text("SELECT 1")).scalar()
    return {"db": "connected", "result": value}
