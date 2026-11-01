import pytest
from backend.app.advisory.guardrails import guardrail

def test_guardrail_passes_grounded_text():
    context = {
        "mandi_price": 4650.0,
        "max_temp": 38.5,
        "min_temp": 23.0
    }
    valid_text = (
        "Soybean in Solapur is under heat stress with maximum temperature of 38.5°C. "
        "Solapur mandi modal price is ₹4,650 per quintal; hold for 2 weeks."
    )
    is_valid, violations = guardrail.validate_grounding(valid_text, context)
    assert is_valid is True
    assert len(violations) == 0

def test_guardrail_rejects_hallucinated_price():
    context = {
        "mandi_price": 4650.0,
        "max_temp": 38.5,
        "min_temp": 23.0
    }
    # Text mentions ₹8,500 which is completely ungrounded
    hallucinated_text = (
        "Soybean prices are booming at ₹8,500 per quintal in Solapur. Sell immediately."
    )
    is_valid, violations = guardrail.validate_grounding(hallucinated_text, context)
    assert is_valid is False
    assert any("Hallucinated price detected" in v for v in violations)

def test_guardrail_rejects_hallucinated_temperature():
    context = {
        "mandi_price": 4650.0,
        "max_temp": 38.5,
        "min_temp": 23.0
    }
    # Text mentions 49°C which is outside 23°C - 38.5°C range
    hallucinated_text = (
        "Severe catastrophic heatwave with temperatures reaching 49°C in Solapur."
    )
    is_valid, violations = guardrail.validate_grounding(hallucinated_text, context)
    assert is_valid is False
    assert any("Hallucinated temperature" in v for v in violations)

