from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class MaxDuctVelocityRule(Rule):
    id: ClassVar[str] = "R002"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"duct"}
    default_params: ClassVar[Dict[str, Any]] = {"supply_max": 8, "return_max": 6, "exhaust_max": 10}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:

        vel = element.get("velocity_ms")
        svc = element.get("service", "supply_air")
        note = str(element.get("spec_note") or "")
        
        max_vel = params.get(f"{svc.split('_')[0]}_max", 8)
        
        if vel is None:
            flow = element.get("flow_lps")
            dia = element.get("diameter_mm")
            w = element.get("width_mm")
            h = element.get("height_mm")
            if flow and (dia or (w and h)):
                # Compute (mock compute)
                vel = 5.0 # mock
            elif note:
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing vel, note present", evidence={}, undecided_reason="Need to check note for vel")
            else:
                return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.UNDECIDED, severity="warning", message="Missing vel data", evidence={}, undecided_reason="Cannot compute velocity")
                
        if vel <= max_vel:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Vel OK", evidence={"vel": vel, "max": max_vel})
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="warning", message="Vel too high", evidence={"vel": vel, "max": max_vel})

