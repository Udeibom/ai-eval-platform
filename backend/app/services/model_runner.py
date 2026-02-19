import requests
import time
from sqlalchemy.orm import Session
from app.config import HF_API_KEY, HF_MODEL
from app import models


HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}


def call_model(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "return_full_text": False
        }
    }

    start = time.time()

    try:
        response = requests.post(HF_URL, headers=headers, json=payload)
        latency = int((time.time() - start) * 1000)

        # Handle non-200 responses
        if response.status_code != 200:
            return f"MODEL_ERROR: {response.text}", latency

        result = response.json()

        # Standard HF text generation response format
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"], latency

        # HF error response format
        if isinstance(result, dict) and "error" in result:
            return f"MODEL_ERROR: {result['error']}", latency

        # Fallback if response shape changes
        return str(result), latency

    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return f"EXCEPTION: {str(e)}", latency


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
