from typing import List, Dict, Any

def check_confidence(llm_decision_dict: Dict[str, Any], conf_threshold: float, override_risk: float, risk_threshold: float) -> str:
    """Returns routing status: 'auto_apply' or 'pending_review' or 'fail_auto'"""
    
    # If the rule engine already failed it, it's auto-applied as FAIL regardless of LLM.
    # (Assuming we pass that logic outside here, but if not we handle it).
    
    if llm_decision_dict.get("verdict") == "NEEDS_HUMAN":
        return "pending_review"
        
    conf = llm_decision_dict.get("confidence", 0.0)
    if conf < conf_threshold:
        return "pending_review"
        
    if override_risk > risk_threshold:
        return "pending_review"
        
    return "auto_apply"
