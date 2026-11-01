import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.app.config import settings

class RAGEngine:
    """RAG-Lite rule retrieval engine indexing ICAR-style agronomic practice guides."""

    def __init__(self):
        self.kb_dir = settings.KNOWLEDGE_BASE_DIR
        self._rules_index: List[Dict[str, Any]] = []
        self._build_index()

    def _build_index(self):
        if not self.kb_dir.exists():
            return
            
        for md_file in self.kb_dir.glob("*.md"):
            crop_name = md_file.stem.lower()
            try:
                content = md_file.read_text(encoding="utf-8")
                # Parse rules separated by ## RULE-
                sections = re.split(r"(##\s+RULE-[A-Z0-9\-]+:?[^\n]*)", content)
                
                current_rule_id = ""
                for s in sections:
                    s_str = s.strip()
                    if s_str.startswith("## RULE-"):
                        current_rule_id = s_str.replace("##", "").strip()
                    elif current_rule_id and s_str:
                        self._rules_index.append({
                            "crop": crop_name,
                            "rule_id": current_rule_id,
                            "text": s_str
                        })
                        current_rule_id = ""
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")

    def retrieve_top_rule(self, crop: str, hazard: str = "drought", stage: str = "") -> Dict[str, Any]:
        crop_norm = crop.strip().lower()
        hazard_norm = hazard.strip().lower()
        
        candidates = [r for r in self._rules_index if r["crop"] == crop_norm]
        if not candidates:
            # Fallback to any rule for crop or generic
            candidates = self._rules_index

        best_rule = candidates[0] if candidates else {
            "crop": crop_norm,
            "rule_id": f"RULE-{crop_norm.upper()}-GENERAL-01",
            "text": "Maintain optimum soil moisture and monitor local weather advisories before applying inputs."
        }

        # Score candidates by matching keywords
        highest_score = -1
        keywords = [hazard_norm]
        if "flood" in hazard_norm or "rain" in hazard_norm:
            keywords.extend(["flood", "waterlogging", "submergence", "drainage"])
        elif "drought" in hazard_norm or "dry" in hazard_norm:
            keywords.extend(["drought", "moisture", "dry spell", "mulch", "deficit"])
        elif "heat" in hazard_norm:
            keywords.extend(["heat", "thermal", "temperature", "spray"])

        for r in candidates:
            rule_text = (r["rule_id"] + " " + r["text"]).lower()
            score = sum(1 for kw in keywords if kw in rule_text)
            if score > highest_score:
                highest_score = score
                best_rule = r

        return best_rule

rag_engine = RAGEngine()

