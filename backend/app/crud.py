from sqlalchemy.orm import Session
from datetime import datetime
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
    return db.query(models.TestSuite).order_by(
        models.TestSuite.created_at.desc()
    ).all()


# -------- Prompts --------

def create_prompt(db: Session, suite_id, prompt: schemas.PromptCreate):
    db_prompt = models.Prompt(
        test_suite_id=suite_id,
        input_text=prompt.input_text,
        expected_output=prompt.expected_output,
        metadata=prompt.metadata or {}  # default to empty dict
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_prompts_by_suite(db: Session, suite_id):
    prompts = db.query(models.Prompt).filter(
        models.Prompt.test_suite_id == suite_id
    ).all()

    # Ensure metadata is a dictionary if it isn't
    for prompt in prompts:
        if isinstance(prompt.metadata_, dict) is False:
            prompt.metadata_ = {}  # Convert to an empty dict if not a dictionary
        # Or use prompt.metadata_.to_dict() if it's a custom object with that method

    return prompts


def get_prompts_by_suite(db: Session, suite_id):
    return db.query(models.Prompt).filter(
        models.Prompt.test_suite_id == suite_id
    ).all()


# -------- Experiments --------

def create_experiment(db: Session, suite_id, model_name, metadata=None):
    exp = models.Experiment(
        test_suite_id=suite_id,
        model_name=model_name,
        model_metadata=metadata,
        status="running",
        started_at=datetime.utcnow()
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


def complete_experiment(db: Session, exp):
    exp.completed_at = datetime.utcnow()

    duration = exp.completed_at - exp.started_at
    exp.duration_ms = int(duration.total_seconds() * 1000)

    exp.status = "completed"

    db.commit()
    db.refresh(exp)
    return exp