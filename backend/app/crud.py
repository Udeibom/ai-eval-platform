from sqlalchemy.orm import Session
from app import models, schemas

# -------- Test Suites --------

def create_test_suite(db: Session, suite: schemas.TestSuiteCreate):
    db_suite = models.TestSuite(
        name=suite.name,
        description=suite.description
    )
    db.add(db_suite)
    db.commit()
    db.refresh(db_suite)
    return db_suite


def get_test_suites(db: Session):
    return db.query(models.TestSuite).order_by(models.TestSuite.created_at.desc()).all()


# -------- Prompts --------

def create_prompt(db: Session, suite_id, prompt: schemas.PromptCreate):
    db_prompt = models.Prompt(
        test_suite_id=suite_id,
        input_text=prompt.input_text,
        expected_output=prompt.expected_output,
        metadata=prompt.metadata
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_prompts_by_suite(db: Session, suite_id):
    return db.query(models.Prompt).filter(
        models.Prompt.test_suite_id == suite_id
    ).all()
