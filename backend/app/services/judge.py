import json
from groq import Groq
from sqlalchemy.orm import Session

from app.config import GROQ_API_KEY, GROQ_JUDGE_MODEL
from app import models
from app.constants import HALLUCINATION_THRESHOLD

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def build_prompt(question: str, answer: str, ground_truth: str | None = None) -> str:
    """
    Builds the evaluation prompt for the judge model.
    """
    return f"""
You are an expert AI evaluator.

Evaluate the MODEL ANSWER using the QUESTION and GROUND TRUTH.

SCORING RULES:
0 = completely incorrect
1 = mostly incorrect
2 = partially correct
3 = mostly correct
4 = correct
5 = perfectly correct

A hallucination occurs if the model invents facts not supported by the ground truth.

QUESTION:
{question}

GROUND TRUTH:
{ground_truth}

MODEL ANSWER:
{answer}

Return ONLY valid JSON:

{{
"score": number,
"hallucination": true or false,
"explanation": "short explanation"
}}
"""


def call_judge(prompt: str) -> str:
    """
    Sends the evaluation prompt to the judge model.
    Returns raw text output.
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_JUDGE_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            top_p=0.9,
            max_tokens=200,
        )

        return response.choices[0].message.content

    except Exception as e:
        return json.dumps(
            {
                "score": 0,
                "hallucination": True,
                "explanation": f"Judge API error: {str(e)}",
            }
        )


def parse_judge_output(text: str) -> dict:
    """
    Attempts to extract and parse JSON from the judge output.
    Falls back to a default failure response if parsing fails.
    """
    try:
        start = text.find("{")
        end = text.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("JSON not found")

        parsed = json.loads(text[start:end])

        return {
            "score": int(parsed.get("score", 0)),
            "hallucination": bool(parsed.get("hallucination", True)),
            "explanation": parsed.get("explanation", "")
        }

    except Exception:
        return {
            "score": 0,
            "hallucination": True,
            "explanation": "Failed to parse judge output"
        }


def evaluate_outputs(db: Session, experiment_id: int) -> None:
    """
    Evaluates all outputs for a given experiment
    and stores evaluation results in the database.
    """
    outputs = (
        db.query(models.Output)
        .filter(models.Output.experiment_id == experiment_id)
        .all()
    )

    for output in outputs:
        question = output.prompt.input_text
        ground_truth = output.prompt.expected_output

        prompt = build_prompt(question, output.output_text, ground_truth)

        raw_response = call_judge(prompt)
        parsed = parse_judge_output(raw_response)

        score = parsed.get("score", 0)
        hallucination_flag = parsed.get("hallucination", True)
        explanation = parsed.get("explanation", "No explanation provided")

        # Avoid double evaluations
        existing = (
            db.query(models.Evaluation)
            .filter(models.Evaluation.output_id == output.id)
            .first()
        )

        if existing:
            continue

        evaluation = models.Evaluation(
            output_id=output.id,
            score=score,
            hallucination=hallucination_flag,
            explanation=explanation,
        )

        db.add(evaluation)

    db.commit()