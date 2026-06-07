from ai.preparation_engine import PreparationEngine
from models.participant import Participant


def test_preparation_fallback(app):
    # create a dummy participant-like object
    class DummyParticipant:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    p = DummyParticipant(1, "Test User")
    engine = PreparationEngine()
    # Ensure fallback generator returns a string even when Gemini unavailable
    text = engine._generate_fallback(p, 0, [], [])
    assert isinstance(text, str)
    assert "Preparation Report" in text


def test_preparation_fallback_sections(app):
    class DummyParticipant:
        def __init__(self, id, name):
            self.id = id
            self.name = name

    p = DummyParticipant(1, "Test User")
    engine = PreparationEngine()

    # Generate fallback with only relationship section
    text = engine._generate_fallback(p, 0, [], [], sections=["relationship"])
    assert "Relationship Summary" in text
    assert "Open Commitments" not in text

    # Generate fallback with only memories section
    text = engine._generate_fallback(p, 0, [], [], sections=["memories"])
    assert "Relationship Summary" not in text
    assert "Suggested Questions" not in text
