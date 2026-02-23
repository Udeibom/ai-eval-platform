import requests
import json
from app.config import HF_API_KEY, HF_JUDGE_MODEL
from sqlalchemy.orm import Session
from app import models

HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_JUDGE_MODEL}"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}



def build_prompt(question, answer, ground_truth=None):
    return f"""
You are an AI evaluator.

Your job is to evaluate the factual correctness of a model response.

Return ONLY valid JSON.

Evaluation criteria:

- score (0-5):
  0 = completely incorrect
  1 = mostly incorrect
  2 = partially correct
  3 = mostly correct
  4 = correct with minor issues
  5 = fully correct

- hallucination:
  true if the answer contains fabricated facts

Evaluate:

QUESTION:
{question}

MODEL ANSWER:
{answer}

GROUND TRUTH:
{ground_truth}

Return JSON:

{{
  "score": number,
  "hallucination": boolean,
  "explanation": "short explanation"
}}
"""



def call_judge(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}

    response = requests.post(HF_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return json.dumps({
            "score": 0,
            "hallucination": True,
            "explanation": f"Judge API error: {response.text}"
        })

    try:
        result = response.json()
    except ValueError:
        raise Exception(
            f"Invalid JSON from HF: {response.text}"
        )

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    return str(result)



def parse_judge_output(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception:
        return {
            "score": 0,
            "hallucination": True,
            "explanation": "Failed to parse judge output"
        }


def evaluate_outputs(db: Session, experiment_id):

    outputs = db.query(models.Output).filter(
        models.Output.experiment_id == experiment_id
    ).all()

    for output in outputs:
        question = output.prompt.input_text
        ground_truth = output.prompt.expected_output

        prompt = build_prompt(question, output.output_text, ground_truth)

        raw = call_judge(prompt)
        parsed = parse_judge_output(raw)

        evaluation = models.Evaluation(
            output_id=output.id,
            score=parsed["score"],
            hallucination=parsed["hallucination"],
            explanation=parsed["explanation"]
        )

        db.add(evaluation)

    db.commit()
