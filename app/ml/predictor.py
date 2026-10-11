from typing import Dict, Any

class OverridePredictor:
    def __init__(self, model_path: str = None):
        self.trained = False
        self.model = None

    def predict_risk(self, element_data: Dict[str, Any], rule_results: list, llm_conf: float) -> float:
        if not self.trained:
            # Fallback when untrained (cold start)
            return 0.1 # neutral/low risk
            
        # In reality, extract features and use self.model.predict_proba
        # (element_type, count_missing, llm_conf, etc.)
        return 0.1
