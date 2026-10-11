import json
from app.llm.schemas import LLMDecision

class Parser:
    @staticmethod
    def parse(response_text: str) -> LLMDecision:
        # Strip markdown fences if present
        text = response_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        data = json.loads(text.strip())
        return LLMDecision.model_validate(data)
