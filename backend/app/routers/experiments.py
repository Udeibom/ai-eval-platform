from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud, models
from app.services.model_runner import run_experiment
from app.services.judge import evaluate_outputs
from app.services.metrics import compute_experiment_metrics

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("/", response_model=schemas.ExperimentResponse)
def create_experiment(
    exp: schemas.ExperimentCreate,
    db: Session = Depends(get_db)
):
    metadata = {
        "provider": "huggingface",
        "temperature": 0.7,
        "max_tokens": 200
    }

    experiment = crud.create_experiment(
        db,
        exp.test_suite_id,
        exp.model_name,
        metadata
    )

    run_experiment(db, experiment)

    evaluate_outputs(db, experiment.id)

    crud.complete_experiment(db, experiment)

    return experiment


@router.get("/{experiment_id}/metrics", response_model=schemas.ExperimentMetrics)
def get_experiment_metrics(
    experiment_id: UUID,
    db: Session = Depends(get_db)
):
    experiment = db.query(models.Experiment).filter(
        models.Experiment.id == experiment_id
    ).first()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    metrics = compute_experiment_metrics(db, experiment_id)

    return {
        "experiment_id": experiment_id,
        "model_name": experiment.model_name,
        **metrics
    }