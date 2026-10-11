# Project Assumptions

- The deterministic engine does not require an asynchronous runtime (`asyncio`). Evaluating rules in memory is fast and CPU-bound, and orchestration logic is cleanly handled by Celery/LangGraph independently.
- The `mock` LLM provider will simply parse the element data and rules using deterministic logic to simulate an LLM. It will evaluate conditions like notes containing "access panel" to decide verdicts. This enables fast and reproducible tests.
- When saving JSON to a file in Python, we'll assume basic `json` serialization is sufficient, though Pydantic is used for request/response serialization to be more robust.
- The default `min_mm` values for rules are illustrative and serve to show difference between clients A and B.
- No real MEP standards are needed; fictional parameters per the spec are perfectly fine and isolate the logic from real-world domain complexity for this demonstration.
- "Synthetic data generation" implies randomness, but we will seed the random number generator (`--seed`) to ensure consistent test sets for regression evaluation.
