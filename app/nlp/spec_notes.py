from typing import Dict, Any, Tuple

def classify_note(note: str) -> Tuple[str, Dict[str, Any]]:
    """
    Returns (category, extracted_entities).
    """
    note_lower = note.lower() if note else ""
    
    entities = {}
    if "access panel" in note_lower:
        entities["access_panel"] = True
    if "firestop" in note_lower:
        entities["firestop"] = True
        
    if not note_lower:
        return "none", entities
        
    if "waiver" in note_lower or "approv" in note_lower:
        return "waiver_approval", entities
    if "exempt" in note_lower:
        return "exemption", entities
    if "alternative" in note_lower or "sleeve" in note_lower:
        return "alternative_method", entities
        
    return "informational", entities
