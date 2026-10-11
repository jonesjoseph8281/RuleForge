from app.graph.workflow import build_workflow
from app.engine.config_resolver import resolve_config

def test_workflow_pass():
    app = build_workflow()
    
    element = {
        "id": "elem-1",
        "type": "duct",
        "clearance_to_ceiling_mm": 200,
        "velocity_ms": 6,
        "service": "supply_air",
        "crosses_fire_wall": False
    }
    
    config = resolve_config("client_A", {})
    
    initial_state = {
        "element": element,
        "resolved_config": config
    }
    
    final_state = app.invoke(initial_state)
    
    assert final_state["final_verdict"] == "PASS"
    assert final_state["route"] == "auto_apply"
    assert "call_llm" not in final_state["trace"]
    
def test_workflow_undecided():
    app = build_workflow()
    
    element = {
        "id": "elem-2",
        "type": "duct",
        "clearance_to_ceiling_mm": 120, # < 150
        "spec_note": "waiver",
        "velocity_ms": 6,
        "service": "supply_air",
        "crosses_fire_wall": False
    }
    
    config = resolve_config("client_A", {})
    config.override_risk_threshold = 0.1
    config.confidence_threshold = 0.90
    
    initial_state = {
        "element": element,
        "resolved_config": config
    }
    
    final_state = app.invoke(initial_state)
    
    # Mock LLM returns PASS with 0.95 conf, Mock risk is 0.05
    assert final_state["final_verdict"] == "PASS"
    assert final_state["route"] == "auto_apply"
    assert "call_llm" in final_state["trace"]
