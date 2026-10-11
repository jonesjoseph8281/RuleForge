from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class EquipmentServiceClearanceRule(Rule):
    id: ClassVar[str] = "R008"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"equipment"}
    default_params: ClassVar[Dict[str, Any]] = {"AHU": 900, "FCU": 600, "pump": 750}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        kind = element.get("kind", "")
        clr = element.get("service_clearance_mm")
        note = str(element.get("spec_note") or "")
        min_clr = params.get(kind, 0)
        
        if min_clr == 0:
             return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Rule disabled for this eq", evidence={})
             
        if clr is None:
             return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing clearance", evidence={}, undecided_reason="No clearance provided")
             
        if clr >= min_clr:
             return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Clearance OK", evidence={"clr": clr, "min": min_clr})
             
        if note:
             return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Clearance low, note present", evidence={"clr": clr, "min": min_clr}, undecided_reason="Check note for waiver")
             
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Clearance too low", evidence={"clr": clr, "min": min_clr})

