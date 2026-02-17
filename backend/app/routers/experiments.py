from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, crud, models
from app.services.model_runner import run_experiment
from app.services.judge import evaluate_outputs  # <-- added import

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/", response_model=schemas.ExperimentResponse)
def create_experiment(exp: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    experiment = crud.create_experiment(db, exp.test_suite_id, exp.model_name)

    run_experiment(db, experiment)

    # <-- added evaluation step
    evaluate_outputs(db, experiment.id)

    crud.update_experiment_status(db, experiment, "completed")

    return experiment
