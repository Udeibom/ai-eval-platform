import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, Integer, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class TestSuite(Base):
    __tablename__ = "test_suites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompts = relationship("Prompt", back_populates="test_suite")


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"))
    input_text = Column(Text, nullable=False)
    expected_output = Column(Text)

    metadata_ = Column("metadata", JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)

    test_suite = relationship("TestSuite", back_populates="prompts")
    outputs = relationship("Output", back_populates="prompt")


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id = Column(String, unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"))
    model_name = Column(String, nullable=False)
    model_metadata = Column(JSON)
    status = Column(String, default="pending")
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    outputs = relationship("Output", back_populates="experiment")


class Output(Base):
    __tablename__ = "outputs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    experiment_id = Column(UUID(as_uuid=True), ForeignKey("experiments.id"))
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"))
    output_text = Column(Text)
    latency_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    experiment = relationship("Experiment", back_populates="outputs")
    prompt = relationship("Prompt", back_populates="outputs")
    evaluations = relationship("Evaluation", back_populates="output")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    output_id = Column(UUID(as_uuid=True), ForeignKey("outputs.id"))
    score = Column(Integer)
    hallucination = Column(Boolean)
    explanation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    output = relationship("Output", back_populates="evaluations")


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_suite_id = Column(UUID(as_uuid=True), ForeignKey("test_suites.id"))
    model_a = Column(String)
    model_b = Column(String)
    total_prompts = Column(Integer)
    experiment_a_id = Column(UUID(as_uuid=True), ForeignKey("experiments.id"), nullable=True)
    experiment_b_id = Column(UUID(as_uuid=True), ForeignKey("experiments.id"), nullable=True)
    status = Column(String, default="running")
    wins_a = Column(Integer)
    wins_b = Column(Integer)
    ties = Column(Integer)
    win_rate_a = Column(Float)
    win_rate_b = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)