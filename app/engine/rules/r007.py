from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class ChilledInsulationRule(Rule):
    id: ClassVar[str] = "R007"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"pipe"}
    default_params: ClassVar[Dict[str, Any]] = {"min_thickness": 25}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        svc = element.get("service", "")
        if svc != "chilled_water":
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Not chilled water", evidence={})
            
        ins = element.get("insulated")
        thick = element.get("insulation_thickness_mm", 0)
        note = str(element.get("spec_note") or "")
        min_t = params.get("min_thickness", 25)
        
        if not ins or thick < min_t:
            if "exempt" in note.lower() or "internal run" in note.lower():
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Insulation fail, note mentions exempt", evidence={}, undecided_reason="Check exemption")
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Insulation missing or thin", evidence={"thick": thick, "min": min_t})
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Insulation OK", evidence={})

