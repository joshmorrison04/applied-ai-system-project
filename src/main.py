"""Command line runner for the Music Recommender Simulation."""

from recommender import load_songs, recommend_songs
from query_parser import parse_user_query
from gemini_client import generate_recommendation
from guardrails import validate_input, calculate_confidence, get_confidence_label, logger


def main() -> None:
    songs = load_songs("data/songs.csv")
    logger.info(f"System started. Loaded {len(songs)} songs.")

    print("\nWelcome to the Music Recommender!")
    print("Describe what kind of music you want.")
    print("Example: 'I want chill music for studying'\n")

    user_query = input("Your request: ").strip()

    # Step 1: Validate input
    is_valid, message = validate_input(user_query)
    if not is_valid:
        logger.warning(f"Invalid input: '{user_query}' — {message}")
        print(f"\n{message}")
        return

    logger.info(f"User query: '{user_query}'")

    # Step 2: Parse the query
    parsed_profile = parse_user_query(user_query)
    logger.info(f"Parsed profile: {parsed_profile}")

    print("\nParsed preferences:")
    print(
        f"  genre={parsed_profile['genre']}, "
        f"mood={parsed_profile['mood']}, "
        f"energy={parsed_profile['energy']}"
    )

    # Step 3: Retrieve top songs
    recommendations = recommend_songs(parsed_profile, songs, k=5)
    logger.info(f"Top recommendation: '{recommendations[0][0]['title']}' (score: {recommendations[0][1]:.2f})")

    print("\nRetrieved songs:")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.2f} | {explanation}")

    # Step 4: Calculate confidence
    confidence = calculate_confidence(parsed_profile, recommendations)
    confidence_label = get_confidence_label(confidence)
    logger.info(f"Confidence: {confidence} ({confidence_label})")

    print(f"\nConfidence: {confidence} ({confidence_label})")

    if confidence_label == "Low":
        print("Note: The system wasn't very confident in these results.")
        print("Try being more specific (e.g., mention a genre, mood, or energy level).")

    # Step 5: Generate AI recommendation
    print("\nGenerating personalized recommendation with Gemini...\n")
    ai_response = generate_recommendation(user_query, recommendations)
    logger.info("Gemini response generated successfully.")

    print("=" * 50)
    print("AI Recommendation:")
    print("=" * 50)
    print(ai_response)


if __name__ == "__main__":
    main()