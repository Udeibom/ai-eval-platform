from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud, models
from app.services.model_runner import run_experiment
from app.services.judge import evaluate_outputs
from app.services.metrics import compute_experiment_metrics
from app.services.comparison import compare_experiments
from app.services.statistics import paired_t_test
from app.services.summary import get_experiment_summary

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.get("/", response_model=list[schemas.ExperimentResponse])
def list_experiments(db: Session = Depends(get_db)):
    experiments = (
        db.query(models.Experiment)
        .filter(models.Experiment.status == "completed")
        .all()
    )
    return experiments


@router.post("/", response_model=schemas.ExperimentResponse)
def create_experiment(
    exp: schemas.ExperimentCreate,
    db: Session = Depends(get_db)
):
    ALLOWED_MODELS = {
        "mixtral-8x7b-32768",
        "llama3-8b-8192",
        "llama-3.3-70b-versatile"
    }

    # Normalize model name
    model_name = exp.model_name.strip().lower()

    if model_name not in ALLOWED_MODELS:
        raise HTTPException(
            status_code=400,
            detail="Model not supported"
        )

    # Prevent duplicate runs
    existing = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.test_suite_id == exp.test_suite_id,
            models.Experiment.model_name == model_name,
            models.Experiment.status == "completed"
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Experiment already exists for this model and test suite"
        )

    metadata = {
        "provider": "groq",
        "temperature": 0.2,
        "max_tokens": 200
    }

    experiment = crud.create_experiment(
        db,
        exp.test_suite_id,
        model_name,
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


@router.get("/compare")
def compare(
    experiment_a: UUID,
    experiment_b: UUID,
    db: Session = Depends(get_db)
):
    result = compare_experiments(db, experiment_a, experiment_b)

    return {
        "experiment_a": experiment_a,
        "experiment_b": experiment_b,
        **result
    }


@router.get("/compare/statistics", response_model=schemas.StatisticalTestResponse)
def compare_stats(
    experiment_a: UUID,
    experiment_b: UUID,
    db: Session = Depends(get_db)
):
    result = paired_t_test(db, experiment_a, experiment_b)

    return {
        "experiment_a": experiment_a,
        "experiment_b": experiment_b,
        **result
    }


@router.get("/{experiment_id}/summary", response_model=schemas.ExperimentSummary)
def experiment_summary(experiment_id: UUID, db: Session = Depends(get_db)):

    experiment = db.query(models.Experiment).filter(
        models.Experiment.id == experiment_id
    ).first()

    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    metrics = get_experiment_summary(db, experiment_id)

    return {
        "experiment_id": experiment.id,
        "run_id": experiment.run_id,
        "model_name": experiment.model_name,
        "status": experiment.status,
        "started_at": experiment.started_at,
        "completed_at": experiment.completed_at,
        "duration_ms": experiment.duration_ms,
        **metrics
    }


@router.get("/summaries")
def all_experiment_summaries(db: Session = Depends(get_db)):
    experiments = (
        db.query(models.Experiment)
        .filter(models.Experiment.status == "completed")
        .all()
    )

    results = []

    for exp in experiments:
        metrics = get_experiment_summary(db, exp.id)

        results.append({
            "experiment_id": exp.id,
            "model_name": exp.model_name,
            **metrics
        })

    return results