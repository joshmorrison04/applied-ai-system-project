# Core recommendation engine: loads song data from CSV and implements
# the scoring logic used to generate recommendations.

import csv
from typing import List, Dict, Tuple


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Scores a single song against user preferences. Returns (score, explanation)."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") is not None and song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_prefs.get("mood") is not None and song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    if user_prefs.get("energy") is not None:
        energy_sim = 1 - abs(user_prefs["energy"] - song["energy"])
        score += energy_sim
        reasons.append(f"energy similarity (+{energy_sim:.2f})")

    if not reasons:
        reasons.append("no strong attribute match")

    explanation = ", ".join(reasons)
    return score, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        total, explanation = score_song(user_prefs, song)
        scored.append((song, total, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]