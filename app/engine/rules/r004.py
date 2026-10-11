from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class DamperAccessRule(Rule):
    id: ClassVar[str] = "R004"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"damper"}
    default_params: ClassVar[Dict[str, Any]] = {}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:
        # All damper elements must have access_panel=True AND access_clearance_mm >= 450mm
        # (BIM exports do not include a 'kind' field; all damper elements are treated as fire/smoke dampers)
        min_clearance_mm = params.get("min_access_clearance_mm", 450)
        access = element.get("access_panel")
        access_clearance = element.get("access_clearance_mm")
        note = str(element.get("spec_note") or "")

        if not access:
            # access_panel is False or missing
            if note:
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="No access panel; spec note present — sending to LLM", evidence={"access_panel": access}, undecided_reason="Missing access panel but note present")
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Access panel missing", evidence={"access_panel": access})

        # access_panel=True; now check clearance
        if access_clearance is not None and access_clearance < min_clearance_mm:
            if note:
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message=f"Access clearance {access_clearance}mm < {min_clearance_mm}mm min; note present", evidence={"access_clearance_mm": access_clearance, "min": min_clearance_mm}, undecided_reason="Insufficient access clearance but note present")
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message=f"Access clearance {access_clearance}mm < {min_clearance_mm}mm minimum required", evidence={"access_clearance_mm": access_clearance, "min": min_clearance_mm})

        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Damper access OK", evidence={"access_panel": access, "access_clearance_mm": access_clearance})

