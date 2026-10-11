from typing import Any, Dict, List
from pydantic import BaseModel
from app.engine.registry import get_all_rules
import app.engine.rules

class ResolvedConfig(BaseModel):
    client_id: str
    enabled_rules: List[str]
    rule_params: Dict[str, Dict[str, Any]]
    confidence_threshold: float
    override_risk_threshold: float = 0.05
    llm_provider: str
    config_hash: str

def resolve_config(client_id: str, design_context: Dict[str, Any]) -> ResolvedConfig:
    """
    Mock config resolver for Phase 1. 
    Later this will read from DB and merge: base -> variant -> overrides.
    """
    all_rules = get_all_rules()
    
    # Base defaults
    rule_params = {
        rule_id: dict(rule_cls.default_params)
        for rule_id, rule_cls in all_rules.items()
    }
    
    # Standard MEP compliance rules: R001-R006
    standard_rules = ["R001", "R002", "R003", "R004", "R005", "R006"]
    enabled_rules = [r for r in standard_rules if r in all_rules]
    
    cid_lower = str(client_id or "").lower()
    
    # Client A: strict (min_mm = 150)
    if "client_a" in cid_lower or "apex" in cid_lower:
        rule_params["R001"]["min_mm"] = 150
        conf = 0.90
        provider = "mock"
    # Client B: relaxed (min_mm = 100)
    elif "client_b" in cid_lower or "beacon" in cid_lower:
        rule_params["R001"]["min_mm"] = 100
        conf = 0.90
        provider = "mock"
    else:
        conf = 0.90
        provider = "mock"

    return ResolvedConfig(
        client_id=client_id,
        enabled_rules=enabled_rules,
        rule_params=rule_params,
        confidence_threshold=conf,
        llm_provider=provider,
        config_hash=f"hash_{client_id}_v1"
    )
