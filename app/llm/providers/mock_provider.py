from app.llm.base import LLMProvider, Message, LLMResponse
from typing import List, Type
from pydantic import BaseModel
import time
import json

class MockProvider(LLMProvider):
    name = "mock"
    
    def complete(self, system: str, messages: List[Message], schema: Type[BaseModel], temperature: float, max_tokens: int, timeout_s: int) -> LLMResponse:
        start_time = time.time()
        
        # Mock logic based on input
        # If "access panel" is in the prompt, return PASS with high confidence.
        # Otherwise NEEDS_HUMAN.
        content = str([m.content.lower() for m in messages])
        
        if "access panel" in content or "waiver" in content:
            verdict = "PASS"
            conf = 0.95
        else:
            verdict = "NEEDS_HUMAN"
            conf = 0.4
            
        mock_output = {
            "verdict": verdict,
            "confidence": conf,
            "reasoning": "Mock evaluation based on keywords in note.",
            "rules_cited": ["R001"],
            "missing_information": [],
            "suggested_action": None
        }
        
        obj = schema.model_validate(mock_output)
        
        latency = int((time.time() - start_time) * 1000)
        
        return LLMResponse(
            raw_text=json.dumps(mock_output),
            parsed_object=obj,
            input_tokens=100,
            output_tokens=50,
            latency_ms=latency,
            model="mock-deterministic",
            provider="mock",
            cost_usd=0.0
        )
