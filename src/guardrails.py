"""Guardrails and reliability features: input validation,
confidence scoring, and logging for the music recommender."""

import logging
import os
from typing import Dict, List, Tuple
from datetime import datetime

# Set up logging to both console and file
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "recommender.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("music_recommender")


def validate_input(user_query: str) -> Tuple[bool, str]:
    """Validates the user's input before processing.
    Returns (is_valid, message)."""

    if not user_query or not user_query.strip():
        return False, "Empty input. Please describe what kind of music you want."

    if len(user_query.strip()) < 3:
        return False, "Input too short. Please provide a more detailed description."

    if len(user_query) > 500:
        return False, "Input too long. Please keep your request under 500 characters."

    return True, "Input is valid."


def calculate_confidence(parsed_profile: Dict, recommendations: List[Tuple[Dict, float, str]]) -> float:
    """Calculates a confidence score (0.0 to 1.0) for the recommendations.
    Based on how many preferences were parsed and how well the top songs matched."""

    score = 0.0

    # How many preferences did we successfully parse? (out of 3)
    parsed_count = sum(1 for v in parsed_profile.values() if v is not None)
    parse_score = parsed_count / 3.0  # 0.0, 0.33, 0.67, or 1.0

    # How strong are the top recommendation scores?
    if recommendations:
        max_possible = 4.0  # genre(2.0) + mood(1.0) + energy(1.0)
        top_score = recommendations[0][1]
        match_score = min(top_score / max_possible, 1.0)
    else:
        match_score = 0.0

    # Weighted combination: parsing matters more than match quality
    score = (parse_score * 0.5) + (match_score * 0.5)

    return round(score, 2)


def get_confidence_label(confidence: float) -> str:
    """Converts a confidence score to a human-readable label."""

    if confidence >= 0.75:
        return "High"
    elif confidence >= 0.45:
        return "Medium"
    else:
        return "Low"