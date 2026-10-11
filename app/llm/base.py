from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class LLMResponse(BaseModel):
    raw_text: str
    parsed_object: Any
    input_tokens: int
    output_tokens: int
    latency_ms: int
    model: str
    provider: str
    cost_usd: float

class LLMProvider(ABC):
    name: str
    
    @abstractmethod
    def complete(self, system: str, messages: List[Message], schema: Type[BaseModel], temperature: float, max_tokens: int, timeout_s: int) -> LLMResponse:
        pass
