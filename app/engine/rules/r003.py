from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class FireWallDamperRule(Rule):
    id: ClassVar[str] = "R003"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"duct"}
    default_params: ClassVar[Dict[str, Any]] = {"rating_margin": 0}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        crosses = element.get("crosses_fire_wall")
        damper_id = element.get("damper_id")
        note = str(element.get("spec_note") or "")
        
        if not crosses:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Does not cross fire wall", evidence={})
            
        if not damper_id:
            if note.strip():
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing fire damper but spec note present — sending to LLM", evidence={}, undecided_reason="Check waiver or alternative method in note")
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="critical", message="Missing fire damper", evidence={})
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Damper present", evidence={"damper_id": damper_id})

