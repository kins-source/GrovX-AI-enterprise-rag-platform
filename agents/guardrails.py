import re
from typing import Tuple
from utils.logger import logger

def is_safe_query(query: str) -> Tuple[bool, str]:
    """
    Validates if the user query is safe and relevant to the allowed domains.
    Reject prompt injection attempts or vastly out-of-domain queries.
    """
    # Define simple heuristics for guardrails
    harmful_keywords = ["ignore all previous instructions", "system prompt", "bypass"]
    query_lower = query.lower()
    
    for kw in harmful_keywords:
        if kw in query_lower:
            logger.warning(f"Guardrail triggered for prompt injection attempt: {query}")
            return False, "Query blocked by security policies."
    
    if len(query) > 1000:
        return False, "Query is too long. Please keep it under 1000 characters."
        
    return True, ""

def validate_grounding(response: str, context: str) -> bool:
    """
    A basic evaluation of whether the response relies on the provided context.
    (In a real production system, this could invoke an LLM-as-a-judge).
    """
    if "i don't know" in response.lower() or "not provided in the context" in response.lower():
        return True
    
    # Just a stub for demonstration: assume true unless explicitly failing some structure
    return True
