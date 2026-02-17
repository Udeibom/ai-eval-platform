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
