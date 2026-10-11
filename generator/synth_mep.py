import argparse
import json
import random
import uuid
import os

def generate_designs(num_designs: int, elements_per_design: int, edge_case_rate: float, out_dir: str, eval_dir: str, seed: int):
    random.seed(seed)
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(eval_dir, exist_ok=True)
    
    labels = []
    
    for d in range(num_designs):
        design_id = f"D-{2026}-{d:04d}"
        elements = []
        
        for e in range(elements_per_design):
            element_id = str(uuid.uuid4())
            is_edge_case = random.random() < edge_case_rate
            client = random.choice(["client_A", "client_B"])
            
            # Simple generation of duct
            el = {
                "id": element_id,
                "type": "duct",
                "level": "L1",
                "clearance_to_ceiling_mm": random.randint(100, 200),
                "velocity_ms": random.randint(5, 12),
                "service": "supply_air",
                "crosses_fire_wall": random.choice([True, False])
            }
            if el["crosses_fire_wall"]:
                el["damper_id"] = "DMP-1" if random.random() > 0.2 else None
                
            expected_verdict = "PASS"
            # Hardcoded label logic for testing
            if el["clearance_to_ceiling_mm"] < 150 and client == "client_A":
                expected_verdict = "FAIL"
            elif el["clearance_to_ceiling_mm"] < 100 and client == "client_B":
                expected_verdict = "FAIL"
                
            if is_edge_case:
                el["spec_note"] = "Approved waiver for reduced clearance with access panel provided."
                if expected_verdict == "FAIL":
                    expected_verdict = "UNDECIDED"
                    
            elements.append(el)
            labels.append({
                "element_id": element_id,
                "client": client,
                "expected_verdict": expected_verdict,
                "expected_rule_ids": ["R001"] # simplified
            })
            
        design = {
            "design_id": design_id,
            "project": f"Project {d}",
            "schema_version": "1.0",
            "units": {"length": "mm", "flow": "L/s", "velocity": "m/s"},
            "rooms": [],
            "elements": elements
        }
        
        with open(os.path.join(out_dir, f"{design_id}.json"), "w") as f:
            json.dump(design, f, indent=2)
            
    with open(os.path.join(eval_dir, "labels.jsonl"), "w") as f:
        for lbl in labels:
            f.write(json.dumps(lbl) + "\n")
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--designs", type=int, default=10)
    parser.add_argument("--elements-per-design", type=int, default=10)
    parser.add_argument("--edge-case-rate", type=float, default=0.15)
    parser.add_argument("--out", type=str, default="data/designs")
    parser.add_argument("--eval", type=str, default="data/eval")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    generate_designs(args.designs, args.elements_per_design, args.edge_case_rate, args.out, args.eval, args.seed)
