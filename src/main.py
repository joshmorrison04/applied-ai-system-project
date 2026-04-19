# Entry point for the application: loads songs, defines user taste profiles,
# runs the recommender scoring logic, and prints the top song recommendations.
"""Command line runner for the Music Recommender Simulation."""

from recommender import load_songs, recommend_songs
from query_parser import parse_user_query
from gemini_client import generate_recommendation


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\nWelcome to the Music Recommender!")
    print("Describe what kind of music you want.")
    print("Example: 'I want chill music for studying'\n")

    user_query = input("Your request: ").strip()

    if not user_query:
        print("You did not enter a request. Please try again.")
        return

    parsed_profile = parse_user_query(user_query)

    print("\nParsed preferences:")
    print(
        f"genre={parsed_profile['genre']}, "
        f"mood={parsed_profile['mood']}, "
        f"energy={parsed_profile['energy']}"
    )

    recommendations = recommend_songs(parsed_profile, songs, k=5)

    print("\nTop recommendations:")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.2f} | {explanation}")
    print()

    print("Generating personalized recommendation with Gemini...\n")
    ai_response = generate_recommendation(user_query, recommendations)
    print("=" * 50)
    print("AI Recommendation:")
    print("=" * 50)
    print(ai_response)


if __name__ == "__main__":
    main()