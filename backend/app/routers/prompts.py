# backend/app/routers/prompts.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.db import get_db
from app import schemas, crud

router = APIRouter(
    prefix="/test-suites/{suite_id}/prompts",
    tags=["Prompts"]
)


@router.post("/", response_model=schemas.PromptResponse)
def add_prompt(
    suite_id: UUID,
    prompt: schemas.PromptCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new prompt for the given test suite.
    """
    return crud.create_prompt(db, suite_id, prompt)


@router.get("/", response_model=list[schemas.PromptResponse])
def list_prompts(
    suite_id: UUID,
    db: Session = Depends(get_db)
):
    """
    List all prompts for a given test suite.
    """
    return crud.get_prompts_by_suite(db, suite_id)