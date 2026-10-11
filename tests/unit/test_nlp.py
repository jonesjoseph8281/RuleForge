from app.nlp.spec_notes import classify_note

def test_classify_note():
    cat, ent = classify_note("Waiver approved with access panel")
    assert cat == "waiver_approval"
    assert ent.get("access_panel") is True
    
    cat, ent = classify_note("No notes")
    assert cat == "informational"
