"""Handles communication with the Google Gemini API for generating
natural-language music recommendations based on retrieved songs."""

import os
from google import genai
from dotenv import load_dotenv
from typing import List, Dict, Tuple

# Load API key from .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(user_query: str, recommendations: List[Tuple[Dict, float, str]]) -> str:
    """Builds the prompt that gets sent to Gemini.
    Takes the user's original query and the retrieved songs with their scores."""

    song_details = ""
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        song_details += (
            f"{i}. \"{song['title']}\" by {song['artist']} "
            f"(Genre: {song['genre']}, Mood: {song['mood']}, Energy: {song['energy']}) "
            f"— Score: {score:.2f}, Reasoning: {explanation}\n"
        )

    prompt = f"""You are a friendly, knowledgeable music recommendation assistant.

A user described what they want to listen to:
"{user_query}"

Based on their request, my retrieval system found these top matches from the catalog:

{song_details}

Using ONLY the songs listed above, write a short, conversational recommendation.
For each song you mention, explain in plain language why it fits what the user asked for.
Do not recommend songs that are not in the list above.
Keep your response concise — no more than a short paragraph per song.
If the matches seem weak, be honest and say the catalog may not have a perfect fit.
Format your response as a numbered list"""

    return prompt


def generate_recommendation(user_query: str, recommendations: List[Tuple[Dict, float, str]]) -> str:
    """Sends the user query + retrieved songs to Gemini and returns
    a conversational recommendation string."""

    prompt = build_prompt(user_query, recommendations)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text

    except Exception as e:
        return f"[Gemini API Error] Could not generate recommendation: {e}"