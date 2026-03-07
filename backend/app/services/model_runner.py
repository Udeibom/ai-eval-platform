import time
from groq import Groq
from sqlalchemy.orm import Session

from app.config import GROQ_API_KEY, GROQ_GENERATION_MODEL
from app import models


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def call_model(model_name: str, prompt: str) -> tuple[str, int]:
    """
    Sends a prompt to the specified Groq model and returns:
    - model response text
    - latency in milliseconds
    """
    start = time.time()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200,
        )

        latency = int((time.time() - start) * 1000)
        output_text = response.choices[0].message.content

        return output_text, latency

    except Exception as e:
        latency = int((time.time() - start) * 1000)
        return f"MODEL_ERROR: {str(e)}", latency


def run_experiment(db: Session, experiment: models.Experiment) -> None:
    """
    Runs the model against all prompts in the experiment's test suite
    and stores the outputs in the database.
    """
    prompts = (
        db.query(models.Prompt)
        .filter(models.Prompt.test_suite_id == experiment.test_suite_id)
        .all()
    )

    for prompt in prompts:
        output_text, latency = call_model(
            experiment.model_name,
            prompt.input_text
        )

        # Skip failed model calls
        if output_text.startswith("MODEL_ERROR"):
            continue

        output = models.Output(
            experiment_id=experiment.id,
            prompt_id=prompt.id,
            output_text=output_text,
            latency_ms=latency,
        )

        db.add(output)

    db.commit()