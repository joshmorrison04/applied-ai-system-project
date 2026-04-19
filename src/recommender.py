# Core recommendation engine: defines the Song and UserProfile data models,
# loads song data from CSV, and implements the scoring logic used to generate recommendations.
import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = []
        for song in self.songs:
            score, _ = score_song(
                {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy},
                {"genre": song.genre, "mood": song.mood, "energy": song.energy, "title": song.title}
            )
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(
            {"genre": user.favorite_genre, "mood": user.favorite_mood, "energy": user.target_energy},
            {"genre": song.genre, "mood": song.mood, "energy": song.energy, "title": song.title}
        )
        return reasons


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
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