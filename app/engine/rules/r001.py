from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class CeilingClearanceRule(Rule):
    id: ClassVar[str] = "R001"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"duct", "pipe"}
    default_params: ClassVar[Dict[str, Any]] = {"min_mm": 150}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        clearance = element.get("clearance_to_ceiling_mm")
        note = str(element.get("spec_note") or "")
        min_mm = params.get("min_mm", 150)
        
        if clearance is None:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing clearance", evidence={}, undecided_reason="No clearance data")
            
        if clearance >= min_mm:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Clearance OK", evidence={"clearance": clearance, "min": min_mm})
            
        # Any non-empty spec_note on a failing element goes to LLM adjudication.
        # The LLM decides: explicit approved waiver → PASS, contradictory/unapproved → FAIL,
        # ambiguous/vague → PENDING_REVIEW (low confidence).
        if note:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Clearance below threshold; spec note present — sending to LLM", evidence={"clearance": clearance, "min": min_mm}, undecided_reason="Spec note requires LLM adjudication")
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Clearance below threshold; no waiver note", evidence={"clearance": clearance, "min": min_mm})

