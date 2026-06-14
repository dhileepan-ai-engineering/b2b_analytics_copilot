import os
import json

class SemanticGlossaryPipeline:
    def __init__(self, glossary_path: str = None):
        # If no custom path is passed, dynamically compute the absolute system path
        if glossary_path is None:
            # Finds the root directory of your project automatically
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.glossary_path = os.path.join(base_dir, "config", "glossary.json")
        else:
            self.glossary_path = glossary_path
            
        self.definitions = self._load_glossary()

    def _load_glossary(self) -> dict:
        if not os.path.exists(self.glossary_path):
            # Temporary safety fallback during tests
            return {
                "MDF": "Marketing Development Funds",
                "VCM": "Vendor Comparison Matrix"
            }
        with open(self.glossary_path, "r") as f:
            return json.load(f)

    def expand_query_context(self, user_query: str) -> str:
        """Scans the query for short-hand corporate acronyms and wraps them into systemic context."""
        matched_contexts = []
        for acronym, definition in self.definitions.items():
            if acronym in user_query.upper():
                matched_contexts.append(f"[{acronym}]: {definition}")
        
        if not matched_contexts:
            return user_query
            
        context_string = "\n".join(matched_contexts)
        expanded_prompt = (
            f"Contextual Domain Glossary expansion mappings discovered for this transaction:\n"
            f"{context_string}\n\n"
            f"User Query to process: {user_query}"
        )
        return expanded_prompt