from typing import Dict, Type
from app.engine.base import Rule

_REGISTRY: Dict[str, Type[Rule]] = {}

def register_rule(rule_cls: Type[Rule]) -> Type[Rule]:
    _REGISTRY[rule_cls.id] = rule_cls
    return rule_cls

def get_rule(rule_id: str) -> Type[Rule]:
    if rule_id not in _REGISTRY:
        raise ValueError(f"Rule {rule_id} not found in registry.")
    return _REGISTRY[rule_id]

def get_all_rules() -> Dict[str, Type[Rule]]:
    return dict(_REGISTRY)
