import pytest
from app.engine.base import Verdict
from app.engine.registry import get_rule, get_all_rules
from app.engine.config_resolver import resolve_config
from app.engine.evaluator import evaluate_element
import app.engine.rules  # Ensures rules are registered

def test_registry():
    rules = get_all_rules()
    assert "R001" in rules
    assert "R009" in rules

def test_config_resolver_client_differences():
    config_a = resolve_config("client_A", {})
    config_b = resolve_config("client_B", {})
    
    assert config_a.rule_params["R001"]["min_mm"] == 150
    assert config_b.rule_params["R001"]["min_mm"] == 100

def test_evaluator_client_a_vs_b():
    element = {
        "id": "elem-1",
        "type": "duct",
        "clearance_to_ceiling_mm": 120,
        "velocity_ms": 6,
        "service": "supply_air",
        "crosses_fire_wall": False
    }
    
    config_a = resolve_config("client_A", {})
    eval_a = evaluate_element(element, config_a)
    
    # R001 should fail for client_A (120 < 150)
    assert eval_a.verdict == Verdict.FAIL
    
    config_b = resolve_config("client_B", {})
    eval_b = evaluate_element(element, config_b)
    
    # R001 should pass for client_B (120 >= 100)
    # Other rules should pass.
    assert eval_b.verdict == Verdict.PASS

def test_evaluator_undecided():
    element = {
        "id": "elem-2",
        "type": "duct",
        "clearance_to_ceiling_mm": 120,
        "velocity_ms": 6,
        "service": "supply_air",
        "crosses_fire_wall": False,
        "spec_note": "waiver approved"
    }
    
    config_a = resolve_config("client_A", {})
    eval_a = evaluate_element(element, config_a)
    
    # R001 should be undecided because of the note and clearance < 150
    assert eval_a.verdict == Verdict.UNDECIDED
