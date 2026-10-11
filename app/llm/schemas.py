from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class LLMDecision(BaseModel):
    verdict: Literal["PASS", "FAIL", "NEEDS_HUMAN"]
    confidence: float = Field(ge=0, le=1)
    reasoning: str
    rules_cited: List[str]
    missing_information: List[str]
    suggested_action: Optional[str] = None
