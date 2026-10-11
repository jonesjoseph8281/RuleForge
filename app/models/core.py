import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Float, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID, ARRAY
from pgvector.sqlalchemy import Vector
from app.core.db import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # admin, engineer, viewer
    api_key_hash = Column(String, nullable=True)
    active = Column(Boolean, default=True)

class RuleDef(Base):
    __tablename__ = "rules"
    id = Column(String, primary_key=True, default=generate_uuid)
    rule_key = Column(String, unique=True, nullable=False)
    description = Column(String)
    severity_default = Column(String)
    current_version = Column(String)

class RuleVariant(Base):
    __tablename__ = "rule_variants"
    id = Column(String, primary_key=True, default=generate_uuid)
    rule_key = Column(String, nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True)
    version = Column(String, nullable=False)
    params = Column(JSONB)
    enabled = Column(Boolean, default=True)
    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    active = Column(Boolean, default=True)

class ClientConfig(Base):
    __tablename__ = "client_configs"
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    version = Column(String, nullable=False)
    confidence_threshold = Column(Float, nullable=False)
    override_risk_threshold = Column(Float, nullable=False)
    llm_provider = Column(String, nullable=False)
    llm_model = Column(String, nullable=False)
    fewshot_k = Column(Integer, default=3)
    retrieval_k = Column(Integer, default=4)
    batch_window_start = Column(String) # e.g. "01:00"
    batch_window_end = Column(String)
    config_hash = Column(String, nullable=False)
    active = Column(Boolean, default=True)

class Design(Base):
    __tablename__ = "designs"
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    external_design_id = Column(String, nullable=False)
    project = Column(String)
    status = Column(String, nullable=False) # uploaded, queued, processing, done, failed
    raw = Column(JSONB)
    element_count = Column(Integer)
    uploaded_by = Column(String)
    uploaded_at = Column(DateTime(timezone=True), default=utc_now)

class Element(Base):
    __tablename__ = "elements"
    id = Column(String, primary_key=True, default=generate_uuid)
    design_id = Column(String, ForeignKey("designs.id"), nullable=False)
    external_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    level = Column(String)
    room_id = Column(String)
    data = Column(JSONB)
    spec_note = Column(Text)

class Batch(Base):
    __tablename__ = "batches"
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, ForeignKey("clients.id"), nullable=True)
    trigger = Column(String)
    status = Column(String, nullable=False)
    window_deadline = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))
    totals = Column(JSONB)

class BatchItem(Base):
    __tablename__ = "batch_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    batch_id = Column(String, ForeignKey("batches.id"), nullable=False)
    element_id = Column(String, ForeignKey("elements.id"), nullable=False)
    idempotency_key = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    attempts = Column(Integer, default=0)
    last_error = Column(Text)
    started_at = Column(DateTime(timezone=True))
    finished_at = Column(DateTime(timezone=True))

class Decision(Base):
    __tablename__ = "decisions"
    id = Column(String, primary_key=True, default=generate_uuid)
    element_id = Column(String, ForeignKey("elements.id"), nullable=False)
    batch_item_id = Column(String, ForeignKey("batch_items.id"), nullable=False)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    final_verdict = Column(String, nullable=False)
    decided_by = Column(String, nullable=False) # rule, llm, human
    status = Column(String, nullable=False) # auto_applied, pending_review, reviewed
    rule_results = Column(JSONB)
    llm_decision = Column(JSONB)
    confidence = Column(Float)
    override_risk = Column(Float)
    config_hash = Column(String)
    prompt_version = Column(String)
    model = Column(String)
    retrieved_chunk_ids = Column(ARRAY(String))
    explanation = Column(Text)
    created_at = Column(DateTime(timezone=True), default=utc_now)

class RuleChunk(Base):
    __tablename__ = "rule_chunks"
    id = Column(String, primary_key=True, default=generate_uuid)
    source = Column(String)
    clause_ref = Column(String)
    text = Column(Text)
    embedding = Column(Vector(384))
    metadata_ = Column("metadata", JSONB)
    content_hash = Column(String)
