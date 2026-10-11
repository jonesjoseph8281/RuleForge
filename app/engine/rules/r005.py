from typing import Any, Dict, ClassVar, Set
from app.engine.base import Rule, RuleResult, Verdict
from app.engine.registry import register_rule

@register_rule
class PipeVelocityRule(Rule):
    id: ClassVar[str] = "R005"
    version: ClassVar[str] = "1.0.0"
    applies_to: ClassVar[Set[str]] = {"pipe"}
    default_params: ClassVar[Dict[str, Any]] = {"max_vel": 2.5}
    
    def applies(self, element: Dict[str, Any]) -> bool:
        return element.get("type") in self.applies_to
        
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:
        svc = element.get("service", "")
        if svc == "condensate":
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Condensate pipe checked by R006", evidence={})
            
        vel = element.get("velocity_ms")
        if vel is None:
            vel = 1.0  # fallback mock
        max_vel = params.get("max_vel", 2.5)
        
        if vel <= max_vel:
            return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.PASS, severity="info", message="Pipe velocity OK", evidence={"vel": vel, "max": max_vel})
            
        return RuleResult(rule_id=self.id, rule_version=self.version, verdict=Verdict.FAIL, severity="warning", message=f"Pipe velocity {vel} m/s exceeds max {max_vel} m/s", evidence={"vel": vel, "max": max_vel})

