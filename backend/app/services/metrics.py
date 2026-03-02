from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def compute_experiment_metrics(db: Session, experiment_id):

    query = (
        db.query(
            func.count(models.Evaluation.id).label("num_samples"),
            func.avg(models.Evaluation.score).label("mean_score"),
            func.stddev(models.Evaluation.score).label("std_dev")
        )
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(models.Output.experiment_id == experiment_id)
    )

    result = query.one()

    return {
        "num_samples": result.num_samples or 0,
        "mean_score": float(result.mean_score or 0),
        "std_dev": float(result.std_dev or 0)
    }