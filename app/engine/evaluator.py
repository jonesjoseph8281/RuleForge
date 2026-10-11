from typing import Any, Dict
from app.engine.base import Verdict, ElementEvaluation, RuleResult
from app.engine.registry import get_rule
from app.engine.config_resolver import ResolvedConfig

def evaluate_element(element: Dict[str, Any], resolved_config: ResolvedConfig) -> ElementEvaluation:
    """
    Evaluates an element against all applicable and enabled rules.
    """
    results = []
    
    for rule_id in resolved_config.enabled_rules:
        rule_cls = get_rule(rule_id)
        rule = rule_cls()
        if rule.applies(element):
            params = resolved_config.rule_params.get(rule_id, rule_cls.default_params)
            context: Dict[str, Any] = {} # Mock context
            res = rule.evaluate(element, params, context)
            results.append(res)
            
    # Combine logic
    final_verdict = Verdict.PASS
    if any(r.verdict == Verdict.FAIL for r in results):
        final_verdict = Verdict.FAIL
    elif any(r.verdict == Verdict.UNDECIDED for r in results):
        final_verdict = Verdict.UNDECIDED
        
    return ElementEvaluation(
        element_id=element.get("id", "unknown"),
        verdict=final_verdict,
        rule_results=results
    )
