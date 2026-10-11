try:
    from langgraph.graph import StateGraph, END
except Exception:
    END = "__end__"
    class StateGraph:
        def __init__(self, state_schema):
            self.state_schema = state_schema
            self.nodes = {}
            self.entry_point = None
            self.conditional_edges = {}
            self.edges = {}

        def add_node(self, name, fn):
            self.nodes[name] = fn

        def set_entry_point(self, name):
            self.entry_point = name

        def add_conditional_edges(self, source, condition_fn, mapping):
            self.conditional_edges[source] = (condition_fn, mapping)

        def add_edge(self, source, target):
            self.edges[source] = target

        def compile(self):
            return self

        def invoke(self, state):
            curr = self.entry_point
            while curr and curr != END:
                fn = self.nodes.get(curr)
                if fn:
                    state = fn(state)
                if curr in self.conditional_edges:
                    cond_fn, mapping = self.conditional_edges[curr]
                    next_node = cond_fn(state)
                    curr = mapping.get(next_node, next_node)
                else:
                    curr = self.edges.get(curr)
            return state

from app.graph.state import ElementState
from app.engine.evaluator import evaluate_element
from app.gate.confidence import check_confidence

def run_rules(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("run_rules")
    eval_res = evaluate_element(state["element"], state["resolved_config"])
    
    # Store results (converting to dict for state ease if needed, or keeping objects)
    state["rule_results"] = [r.model_dump() for r in eval_res.rule_results]
    
    if eval_res.verdict != "UNDECIDED":
        state["final_verdict"] = eval_res.verdict.value
        state["route"] = "auto_apply"
    else:
        state["final_verdict"] = "UNDECIDED"
        
    return state

def should_call_llm(state: ElementState) -> str:
    if state.get("final_verdict") == "UNDECIDED":
        return "retrieve_context"
    return "finalize"

def retrieve_context(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("retrieve_context")
    state["retrieved_chunks"] = ["chunk-1"] # mock
    return state

def classify_waiver_note(note: str) -> str:
    note_lower = (note or "").lower().strip()
    if not note_lower:
        return ""
    if "not yet approved" in note_lower or "unapproved" in note_lower or "rejected" in note_lower or "pending" in note_lower:
        return "contradictory"
    if "approved" in note_lower or "accepted by" in note_lower or "signed off" in note_lower or "waiver" in note_lower:
        return "explicit"
    return "ambiguous"

def call_llm(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("call_llm")
    el = state.get("element", {})
    note = str(el.get("spec_note") or "")
    note_class = classify_waiver_note(note)
    
    if note_class == "explicit":
        verdict = "PASS"
        conf = 0.95
        reason = "Explicit approved waiver cited with engineering sign-off."
    elif note_class == "contradictory":
        verdict = "FAIL"
        conf = 0.95
        reason = "Spec note contradicts compliance: waiver requested but NOT yet approved."
    else: # ambiguous
        verdict = "NEEDS_HUMAN"
        conf = 0.75
        reason = "Ambiguous installation/site note does not provide formal waiver approval."

    state["llm_decision"] = {
        "verdict": verdict,
        "confidence": conf,
        "reasoning": reason,
        "rules_cited": [r["rule_id"] for r in state.get("rule_results", []) if r.get("verdict") == "UNDECIDED"],
        "waiver_note_class": note_class
    }
    state["confidence"] = conf
    state["waiver_note_class"] = note_class
    return state

def score_override_risk(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("score_override_risk")
    state["override_risk"] = 0.05
    return state
    
def confidence_gate(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("confidence_gate")
    conf_thresh = getattr(state["resolved_config"], "confidence_threshold", 0.90)
    risk_thresh = getattr(state["resolved_config"], "override_risk_threshold", 0.10)
    
    route = check_confidence(
        state["llm_decision"], 
        conf_thresh,
        state["override_risk"],
        risk_thresh
    )
    
    state["route"] = route
    if route == "pending_review":
        state["final_verdict"] = "PENDING_REVIEW"
    else:
        state["final_verdict"] = state["llm_decision"]["verdict"]
        
    return state

def finalize(state: ElementState) -> ElementState:
    state.setdefault("trace", []).append("finalize")
    return state

def build_workflow() -> StateGraph:
    workflow = StateGraph(ElementState)
    
    workflow.add_node("run_rules", run_rules)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("call_llm", call_llm)
    workflow.add_node("score_override_risk", score_override_risk)
    workflow.add_node("confidence_gate", confidence_gate)
    workflow.add_node("finalize", finalize)
    
    workflow.set_entry_point("run_rules")
    
    workflow.add_conditional_edges("run_rules", should_call_llm, {
        "retrieve_context": "retrieve_context",
        "finalize": "finalize"
    })
    
    workflow.add_edge("retrieve_context", "call_llm")
    workflow.add_edge("call_llm", "score_override_risk")
    workflow.add_edge("score_override_risk", "confidence_gate")
    workflow.add_edge("confidence_gate", "finalize")
    workflow.add_edge("finalize", END)
    
    return workflow.compile()
