import re
from typing import Dict, Any, List, Tuple

class GroundingGuardrail:
    """Validates that advisory outputs never hallucinate prices or weather metrics outside structured context."""

    def validate_grounding(
        self,
        generated_text: str,
        verified_context: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        violations = []
        
        # 1. Check Price Grounding (look for ₹ or Rs. numbers)
        price_patterns = re.findall(r"(?:₹|Rs\.?)\s*([0-9]+(?:,[0-9]+)?)", generated_text)
        verified_price = verified_context.get("mandi_price")
        
        if price_patterns:
            for p_str in price_patterns:
                p_val = float(p_str.replace(",", ""))
                # Allow minor tolerance or exact match
                if verified_price:
                    diff = abs(p_val - float(verified_price))
                    if diff > 10.0: # Mismatch > ₹10
                        violations.append(
                            f"Hallucinated price detected: ₹{p_val:.0f} found in text, but verified mandi price is ₹{verified_price:.0f}."
                        )
                else:
                    violations.append(f"Price ₹{p_val:.0f} cited without verified price context.")

        # 2. Check Temperature Grounding (look for XX°C)
        temp_patterns = re.findall(r"([0-9]+(?:\.[0-9]+)?)\s*°\s*C", generated_text, re.IGNORECASE)
        max_t = verified_context.get("max_temp")
        min_t = verified_context.get("min_temp")
        curr_t = verified_context.get("current_temp")
        valid_temps = [t for t in [max_t, min_t, curr_t] if t is not None]

        if temp_patterns and valid_temps:
            for t_str in temp_patterns:
                t_val = float(t_str)
                # Check if matches any valid temperature within 2 degrees
                matched = any(abs(t_val - float(vt)) <= 2.0 for vt in valid_temps)
                if not matched:
                    violations.append(
                        f"Hallucinated temperature: {t_val}°C found, but valid context range is {min(valid_temps):.1f}°C to {max(valid_temps):.1f}°C."
                    )

        is_valid = len(violations) == 0
        return is_valid, violations

guardrail = GroundingGuardrail()

