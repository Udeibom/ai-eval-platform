from app.db import SessionLocal
from app import models
import uuid

db = SessionLocal()

suite = models.TestSuite(
    id=uuid.uuid4(),
    name="Basic Knowledge",
    description="Sanity check prompts"
)

db.add(suite)
db.commit()
db.refresh(suite)

prompts = [
    models.Prompt(
        test_suite_id=suite.id,
        input_text="Who wrote Hamlet?",
        expected_output="William Shakespeare"
    ),
    models.Prompt(
        test_suite_id=suite.id,
        input_text="What is the capital of Germany?",
        expected_output="Berlin"
    )
]

db.add_all(prompts)
db.commit()

print("Seed complete. Suite ID:", suite.id)
