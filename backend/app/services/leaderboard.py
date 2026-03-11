from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models


def get_leaderboard(db: Session):

    results = (
        db.query(
            models.Experiment.model_name.label("model"),

            func.avg(models.Evaluation.score).label("mean_score"),

            func.avg(
                func.cast(models.Evaluation.hallucination, func.Integer)
            ).label("hallucination_rate"),

            func.avg(models.Output.latency_ms).label("avg_latency"),

            func.count(models.Evaluation.id).label("samples"),

            func.avg(
                func.case(
                    (models.Evaluation.score >= 4, 1),
                    else_=0
                )
            ).label("pass_rate"),
        )
        .join(models.Output, models.Output.experiment_id == models.Experiment.id)
        .join(models.Evaluation, models.Evaluation.output_id == models.Output.id)
        .group_by(models.Experiment.model_name)
        .order_by(func.avg(models.Evaluation.score).desc())
    )

    leaderboard = []

    for row in results:

        leaderboard.append({
            "model": row.model,
            "mean_score": float(row.mean_score or 0),
            "hallucination_rate": float(row.hallucination_rate or 0),
            "avg_latency": float(row.avg_latency or 0),
            "pass_rate": float(row.pass_rate or 0),
            "samples": int(row.samples or 0)
        })

    return leaderboard