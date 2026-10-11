from typing import Dict, Any

def ingest_correction(decision_id: str, client_id: str, corrected_verdict: str, reason_code: str, comment: str) -> Dict[str, Any]:
    # Mock database insertion
    # In reality, this updates the Decision to 'reviewed'
    # And inserts a Correction record.
    return {
        "status": "success",
        "correction_id": "c-123",
        "decision_id": decision_id
    }
