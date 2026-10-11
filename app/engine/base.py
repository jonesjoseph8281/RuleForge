from enum import Enum
from typing import Any, ClassVar, Dict, Set, Optional, List
from pydantic import BaseModel
from abc import ABC, abstractmethod

class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNDECIDED = "UNDECIDED"

class RuleResult(BaseModel):
    rule_id: str
    rule_version: str
    verdict: Verdict
    severity: str
    message: str
    evidence: Dict[str, Any]
    undecided_reason: Optional[str] = None

class ElementEvaluation(BaseModel):
    element_id: str
    verdict: Verdict
    rule_results: List[RuleResult]

class Rule(ABC):
    id: ClassVar[str]
    version: ClassVar[str]
    applies_to: ClassVar[Set[str]]
    default_params: ClassVar[Dict[str, Any]]
    
    @abstractmethod
    def applies(self, element: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def evaluate(self, element: Dict[str, Any], params: Dict[str, Any], context: Dict[str, Any]) -> RuleResult:
        pass
