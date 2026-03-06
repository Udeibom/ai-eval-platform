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
    metadata: dict = {}
    created_at: datetime

    class Config:
        from_attributes = True


# -------- Experiment --------

class ExperimentCreate(BaseModel):
    test_suite_id: UUID
    model_name: str


class RunComparisonRequest(BaseModel):
    test_suite_id: UUID
    model_a: str
    model_b: str

class ExperimentResponse(BaseModel):
    id: UUID
    run_id: str
    test_suite_id: UUID
    model_name: str
    status: str
    started_at: datetime | None
    completed_at: datetime | None
    duration_ms: int | None

    class Config:
        from_attributes = True


class ExperimentMetrics(BaseModel):
    experiment_id: UUID
    model_name: str
    num_samples: int
    mean_score: float
    std_dev: float


class ComparisonResponse(BaseModel):
    experiment_a: UUID
    experiment_b: UUID
    total_prompts: int
    wins_a: int
    wins_b: int
    ties: int
    win_rate_a: float
    win_rate_b: float

class StatisticalTestResponse(BaseModel):
    experiment_a: UUID
    experiment_b: UUID
    t_statistic: float
    p_value: float
    significant: bool

class ExperimentSummary(BaseModel):
    experiment_id: UUID
    run_id: str
    model_name: str
    status: str

    num_samples: int
    mean_score: float
    std_dev: float
    hallucination_rate: float

    avg_latency: float
    max_latency: int
    min_latency: int

    started_at: datetime | None
    completed_at: datetime | None
    duration_ms: int | None

class ComparisonJobResponse(BaseModel):
    id: UUID
    status: str

    class Config:
        from_attributes = True