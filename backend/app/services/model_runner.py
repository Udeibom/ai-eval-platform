import requests
import time
from sqlalchemy.orm import Session
from app.config import HF_API_KEY, HF_MODEL
from app import models

HF_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def call_model(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }

    start = time.time()
    response = requests.post(HF_URL, headers=headers, json=payload)
    latency = int((time.time() - start) * 1000)

    result = response.json()

    text = result[0]["generated_text"] if isinstance(result, list) else str(result)

    return text, latency


def run_experiment(db: Session, experiment: models.Experiment):
    prompts = db.query(models.Prompt).filter(
        models.Prompt.test_suite_id == experiment.test_suite_id
    ).all()

    for prompt in prompts:
        output_text, latency = call_model(prompt.input_text)

        output = models.Output(
            experiment_id=experiment.id,
            prompt_id=prompt.id,
            output_text=output_text,
            latency_ms=latency
        )

        db.add(output)

    db.commit()
