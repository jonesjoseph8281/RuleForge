import pytest
from app.llm.schemas import LLMDecision
from app.llm.base import Message
from app.llm.providers.mock_provider import MockProvider
from app.llm.parser import Parser
from app.gate.confidence import check_confidence
from pydantic import ValidationError

def test_mock_provider_access_panel():
    provider = MockProvider()
    resp = provider.complete(
        system="test", 
        messages=[Message(role="user", content="note: access panel provided")], 
        schema=LLMDecision, 
        temperature=0.0, 
        max_tokens=100, 
        timeout_s=5
    )
    assert resp.parsed_object.verdict == "PASS"
    assert resp.parsed_object.confidence == 0.95

def test_mock_provider_needs_human():
    provider = MockProvider()
    resp = provider.complete(
        system="test", 
        messages=[Message(role="user", content="note: weird stuff")], 
        schema=LLMDecision, 
        temperature=0.0, 
        max_tokens=100, 
        timeout_s=5
    )
    assert resp.parsed_object.verdict == "NEEDS_HUMAN"

def test_parser_markdown_fences():
    text = "```json\n{\"verdict\": \"FAIL\", \"confidence\": 0.9, \"reasoning\": \"x\", \"rules_cited\": [], \"missing_information\": []}\n```"
    decision = Parser.parse(text)
    assert decision.verdict == "FAIL"

def test_confidence_gate():
    d1 = {"verdict": "PASS", "confidence": 0.95}
    assert check_confidence(d1, 0.90, 0.1, 0.2) == "auto_apply"
    
    d2 = {"verdict": "PASS", "confidence": 0.85}
    assert check_confidence(d2, 0.90, 0.1, 0.2) == "pending_review"
    
    d3 = {"verdict": "NEEDS_HUMAN", "confidence": 0.99}
    assert check_confidence(d3, 0.90, 0.1, 0.2) == "pending_review"
    
    d4 = {"verdict": "PASS", "confidence": 0.95}
    # Risk too high
    assert check_confidence(d4, 0.90, 0.3, 0.2) == "pending_review"
