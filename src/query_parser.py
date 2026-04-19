"""Parses natural-language music requests into structured user preferences."""

from typing import Dict
from keyword_maps import GENRE_KEYWORDS, MOOD_KEYWORDS, ENERGY_KEYWORDS


def parse_user_query(query: str) -> Dict[str, object]:
    """
    Converts a natural-language music request into structured preferences.

    Returns a dictionary with:
    - genre
    - mood
    - energy
    """
    query_lower = query.lower()

    parsed = {
        "genre": None,
        "mood": None,
        "energy": None,
    }

    for phrase, genre in sorted(GENRE_KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase in query_lower:
            parsed["genre"] = genre
            break

    for phrase, mood in sorted(MOOD_KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase in query_lower:
            parsed["mood"] = mood
            break

    for phrase, energy in sorted(ENERGY_KEYWORDS.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase in query_lower:
            parsed["energy"] = energy
            break

    return parsed