"""Streamlit UI for the AI Music Recommender."""

import streamlit as st
from recommender import load_songs, recommend_songs
from query_parser import parse_user_query
from gemini_client import generate_recommendation
from guardrails import validate_input, calculate_confidence, get_confidence_label, logger

# Page config
st.set_page_config(page_title="AI Music Recommender", page_icon="🎵", layout="centered")

st.title("🎵 AI Music Recommender")
st.write("Describe what kind of music you want, and I'll find the perfect songs for you.")

# Load songs once
@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")

songs = get_songs()

# User input
user_query = st.text_input("What kind of music are you looking for?", placeholder="e.g. I want chill jazz for studying")

if st.button("Get Recommendations") and user_query:

    # Validate
    is_valid, message = validate_input(user_query)
    if not is_valid:
        st.error(message)
    else:
        logger.info(f"User query: '{user_query}'")

        # Parse
        parsed = parse_user_query(user_query)
        logger.info(f"Parsed profile: {parsed}")

        st.subheader("Parsed Preferences")
        cols = st.columns(3)
        cols[0].metric("Genre", parsed["genre"] or "Not detected")
        cols[1].metric("Mood", parsed["mood"] or "Not detected")
        cols[2].metric("Energy", parsed["energy"] or "Not detected")

        # Retrieve
        recommendations = recommend_songs(parsed, songs, k=5)
        logger.info(f"Top recommendation: '{recommendations[0][0]['title']}' (score: {recommendations[0][1]:.2f})")

        # Confidence
        confidence = calculate_confidence(parsed, recommendations)
        confidence_label = get_confidence_label(confidence)
        logger.info(f"Confidence: {confidence} ({confidence_label})")

        if confidence_label == "High":
            st.success(f"Confidence: {confidence} ({confidence_label})")
        elif confidence_label == "Medium":
            st.warning(f"Confidence: {confidence} ({confidence_label})")
        else:
            st.error(f"Confidence: {confidence} ({confidence_label}) — Try being more specific.")

        # Show retrieved songs
        st.subheader("Retrieved Songs")
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            with st.expander(f"{i}. {song['title']} by {song['artist']} — Score: {score:.2f}"):
                st.write(f"**Genre:** {song['genre']} | **Mood:** {song['mood']} | **Energy:** {song['energy']}")
                st.write(f"**Why:** {explanation}")

        # Generate AI recommendation
        st.subheader("AI Recommendation")
        with st.spinner("Generating personalized recommendation..."):
            ai_response = generate_recommendation(user_query, recommendations)
            logger.info("Gemini response generated successfully.")
        st.markdown(ai_response)