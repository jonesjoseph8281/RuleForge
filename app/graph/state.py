from typing import TypedDict, List, Dict, Any, Optional
from app.engine.config_resolver import ResolvedConfig

class ElementState(TypedDict, total=False):
    element: Dict[str, Any]
    resolved_config: ResolvedConfig
    rule_results: List[Dict[str, Any]]
    llm_attempts: int
    retrieved_chunks: List[str]
    fewshot_examples: List[Dict[str, Any]]
    llm_decision: Optional[Dict[str, Any]]
    override_risk: float
    confidence: float
    final_verdict: str
    route: str # auto_apply, pending_review, dead_letter
    errors: List[str]
    trace: List[str]
