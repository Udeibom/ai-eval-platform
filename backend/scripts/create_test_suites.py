from app.db import SessionLocal
from app import models

db = SessionLocal()

suites = [
    {
        "name": "factual_suite",
        "description": "Factual question answering evaluation"
    },
    {
        "name": "reasoning_suite",
        "description": "Logical and mathematical reasoning evaluation"
    },
    {
        "name": "instruction_suite",
        "description": "Instruction following evaluation"
    }
]

for s in suites:

    suite = models.TestSuite(
        name=s["name"],
        description=s["description"]
    )

    db.add(suite)

db.commit()

print("Test suites created successfully")