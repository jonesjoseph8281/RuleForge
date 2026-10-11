from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class CondensateSlopeRule(Rule):
    id: ClassVar[str] = "R006"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"pipe"}
    default_params: ClassVar[Dict[str, Any]] = {"min_slope": 1.0}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        svc = element.get("service", "")
        if svc != "condensate":
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Not condensate", evidence={})
            
        slope = element.get("slope_pct")  # field name in BIM export is slope_pct
        note = str(element.get("spec_note") or "")
        min_slope = params.get("min_slope", 1.0)
        
        if slope is None:
            if note:
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing slope, note present", evidence={}, undecided_reason="Check note for slope")
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Missing slope data", evidence={})
            
        if slope >= min_slope:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Slope OK", evidence={"slope": slope, "min": min_slope})
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Slope too low", evidence={"slope": slope, "min": min_slope})

