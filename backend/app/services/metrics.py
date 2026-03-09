from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def compute_experiment_metrics(db: Session, experiment_id):

    query = (
        db.query(
            func.count(models.Evaluation.id).label("num_samples"),
            func.avg(models.Evaluation.score).label("mean_score"),
            func.stddev(models.Evaluation.score).label("std_dev"),
            func.avg(models.Output.latency_ms).label("avg_latency")
        )
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(models.Output.experiment_id == experiment_id)
    )

    result = query.one()

    hallucinations = (
        db.query(func.count(models.Evaluation.id))
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(
            models.Output.experiment_id == experiment_id,
            models.Evaluation.score < 0.5
        )
        .scalar()
    )

    num_samples = result.num_samples or 0

    hallucination_rate = 0
    if num_samples > 0:
        hallucination_rate = hallucinations / num_samples

    return {
        "num_samples": num_samples,
        "mean_score": float(result.mean_score or 0),
        "std_dev": float(result.std_dev or 0),
        "avg_latency": float(result.avg_latency or 0),
        "hallucination_rate": float(hallucination_rate)
    }