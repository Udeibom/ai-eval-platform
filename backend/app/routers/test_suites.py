from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, crud

router = APIRouter(prefix="/test-suites", tags=["Test Suites"])


@router.post("/", response_model=schemas.TestSuiteResponse)
def create_suite(suite: schemas.TestSuiteCreate, db: Session = Depends(get_db)):
    return crud.create_test_suite(db, suite)


@router.get("/", response_model=list[schemas.TestSuiteResponse])
def list_suites(db: Session = Depends(get_db)):
    return crud.get_test_suites(db)
