# Design Decisions

## 1. Rules First, LLM Last
**Context:** LLMs are expensive, prone to hallucination, and slow. MEP checks are mostly deterministic (e.g. clearance > 150mm).
**Decision:** We use a pure Python deterministic engine to evaluate all elements first. The LLM only receives elements that produce an `UNDECIDED` verdict (usually because of a missing field explained away by a free-text note).
**Trade-offs:** We have to manually code rules, which takes initial engineering effort, but saves massive compute resources and ensures 100% explainability for standard cases.

## 2. Configurable Variants over Bespoke Code
**Context:** Client A and Client B have different standards.
**Decision:** We store parameters (e.g., `min_mm`) and confidence thresholds in the DB per client, merging them at runtime via `config_resolver`.
**Trade-offs:** DB lookups per batch. Mitigated by resolving config once per batch/design context.

## 3. Python 3.11 + Type Hinting
**Context:** Data validation and ML orchestration.
**Decision:** We enforce `pydantic` and Python 3.11 modern type hinting (`dict[str, Any]` natively, etc.) in production.
**Note:** Local tests might fail if run on Python 3.8; Docker provides the official runtime.
