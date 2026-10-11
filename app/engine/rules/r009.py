from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class MissingDataRule(Rule):
    """
    R009: Missing Data
    Intent: Ensure required fields for applicable rules are present.
    """
    id: ClassVar[str] = "R009"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"duct", "pipe", "damper", "equipment"}
    default_params: ClassVar[Dict[str, Any]] = {}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return True
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:
        # Simplified: checking basic required fields.
        reqs = ["id", "type"]
        missing = [r for r in reqs if element.get(r) is None]
        
        # Specific rule data requirements will be checked in specific rules which return UNDECIDED.
        # R009 acts as a basic structure checker here, or can be made complex.
        if missing:
            return RuleResult(
                rule_id=self.id, rule_version=self.version,
                verdict=Verdict.UNDECIDED, severity="critical",
                message=f"Missing required fields: {missing}",
                evidence={"missing": missing},
                undecided_reason="Missing fields cannot be derived"
            )
            
        return RuleResult(
            rule_id=self.id, rule_version=self.version,
            verdict=Verdict.PASS, severity="info",
            message="Required base fields present",
            evidence={}
        )
