from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# -------- Test Suite --------

class TestSuiteCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TestSuiteResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# -------- Prompt --------

class PromptCreate(BaseModel):
    input_text: str
    expected_output: Optional[str] = None
    metadata: Optional[dict] = None

class PromptResponse(BaseModel):
    id: UUID
    input_text: str
    expected_output: Optional[str]
    metadata: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


# -------- Experiment --------

class ExperimentCreate(BaseModel):
    test_suite_id: UUID
    model_name: str

class ExperimentResponse(BaseModel):
    id: UUID
    test_suite_id: UUID
    model_name: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
