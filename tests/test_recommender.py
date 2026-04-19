# Unit tests for the recommender module: verifies that song loading, scoring,
# and recommendation logic behave correctly using standalone functions.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from recommender import load_songs, score_song, recommend_songs

def test_genre_match_adds_points():
    user = {"genre": "pop", "mood": None, "energy": None}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "title": "Test"}
    score, explanation = score_song(user, song)
    assert score == 2.0
    assert "genre match" in explanation


def test_mood_match_adds_points():
    user = {"genre": None, "mood": "chill", "energy": None}
    song = {"genre": "lofi", "mood": "chill", "energy": 0.4, "title": "Test"}
    score, explanation = score_song(user, song)
    assert score == 1.0
    assert "mood match" in explanation


def test_energy_similarity_scoring():
    user = {"genre": None, "mood": None, "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "title": "Test"}
    score, explanation = score_song(user, song)
    assert score == 1.0
    assert "energy similarity" in explanation


def test_full_match_scores_highest():
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "title": "Test"}
    score, _ = score_song(user, song)
    assert score == 4.0


def test_no_preferences_returns_zero():
    user = {"genre": None, "mood": None, "energy": None}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "title": "Test"}
    score, explanation = score_song(user, song)
    assert score == 0.0
    assert "no strong attribute match" in explanation


def test_recommend_songs_returns_sorted():
    songs = [
        {"genre": "lofi", "mood": "chill", "energy": 0.4, "title": "Song A", "artist": "A"},
        {"genre": "pop", "mood": "happy", "energy": 0.8, "title": "Song B", "artist": "B"},
    ]
    user = {"genre": "pop", "mood": "happy", "energy": 0.8}
    results = recommend_songs(user, songs, k=2)
    assert results[0][0]["title"] == "Song B"
    assert results[0][1] > results[1][1]