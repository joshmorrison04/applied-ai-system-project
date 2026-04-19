# Model Card — AI Music Recommender

## 1. Model Name

AI Music Recommender

## 2. Intended Use

This system provides personalized music recommendations based on natural language input. A user describes what kind of music they want (e.g., "I want chill jazz for studying"), and the system retrieves relevant songs from a curated dataset and uses Google Gemini to generate a conversational recommendation. It is intended for classroom demonstration and portfolio purposes only, not for production use with real users.

## 3. How It Works

The system follows a RAG (Retrieval-Augmented Generation) pipeline. First, the user's natural language request is parsed into structured preferences — genre, mood, and energy level — using keyword-based matching. Then, the recommender scores every song in the dataset against those preferences: +2.0 points for a genre match, +1.0 for a mood match, and up to +1.0 based on how close the song's energy level is to what the user wants. The top 5 scoring songs are retrieved and passed to Google Gemini along with the user's original query. Gemini then writes a friendly, conversational recommendation explaining why each song fits. A confidence score is also calculated based on how many preferences were successfully parsed and how strong the top matches are.

## 4. Data

The dataset consists of 56 songs stored in a CSV file. Each song has 10 attributes: ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The scoring logic currently uses only genre, mood, and energy. The dataset was expanded from an original set of 20 songs to include a wider range of genres (pop, rock, lofi, jazz, ambient, electronic, r&b, classical, metal, synthwave, folk, funk, alternative, world, indie pop, hip-hop, latin) and moods (happy, chill, relaxed, focused, intense, energetic, moody, melancholy). The dataset was curated by the developer and reflects a broad but not exhaustive range of musical styles. Some genres and regional music traditions are underrepresented or absent.

## 5. Strengths

The system works well when the user provides clear, specific requests that align with keywords in the parser's dictionaries. For queries like "I want chill jazz for studying," the system correctly identifies genre (jazz), mood (focused), and energy (0.4), retrieves highly relevant songs, and generates a helpful recommendation with High confidence. The RAG architecture keeps recommendations grounded in real data — the AI can only recommend songs that exist in the dataset, preventing hallucination. The confidence scoring system provides useful transparency, letting users know when the system is less sure about its results. Logging provides a full audit trail of every interaction for debugging and reliability review.

## 6. Limitations and Bias

The keyword-based parser is the biggest limitation. It relies on exact or near-exact matches to predefined dictionaries, so it misses synonyms, uncommon phrasings, and natural variations. For example, "happy" is recognized but "happiness" is not. "Relaxed" is recognized but "relaxing" had to be manually added after testing revealed the gap. This means the quality of recommendations depends heavily on whether the user happens to use words that are in the dictionaries.

The dataset reflects the developer's musical knowledge and is biased toward Western, English-language music. Genres like K-pop, Afrobeats, reggaeton, and Bollywood are not represented, which means users who prefer those styles will get poor recommendations based solely on energy proximity rather than genuine relevance.

The scoring system treats genre as the most important factor (2.0 points vs 1.0 for mood), which means a song in the right genre but with the wrong mood will outscore a perfect mood match in a different genre. This weighting may not reflect every user's actual priorities.

The system also depends on an external API (Google Gemini) which can experience rate limits, outages, or quota restrictions. During development, the Gemini 2.0 Flash model became unavailable on the free tier, requiring a switch to Gemini 2.5 Flash.

## 7. Potential Misuse and Prevention

The system itself poses low risk since it only recommends songs from a fixed, curated dataset. However, potential misuse scenarios include:

Prompt injection — a user could try to manipulate the Gemini prompt to make the AI say something unrelated to music. The system mitigates this by constraining the prompt with clear instructions ("Using ONLY the songs listed above") and by validating input length (max 500 characters).

Biased curation — if the dataset were intentionally filled with songs promoting harmful content, the system would surface those recommendations. This is mitigated by the developer curating the dataset manually and reviewing all song entries.

Over-reliance — a user might assume the system's recommendations represent the full landscape of music, when in reality it only knows about 56 songs. The confidence scoring helps signal when results may not be strong.

## 8. Testing Results

The system was tested across a range of scenarios: specific queries with clear genre/mood/energy keywords, vague queries with minimal information, empty and too-short inputs, and queries using words not in the keyword dictionaries. Input validation correctly blocked empty and too-short inputs. Confidence scoring accurately reflected recommendation quality — specific queries scored High (0.75+) while vague queries scored Low (below 0.45). The main failure mode was the parser returning None for all three preferences when the user's language didn't match any dictionary keywords, resulting in essentially random song selection. All runs were logged to recommender.log for review.

## 9. AI Collaboration Reflection

I used AI assistants (Claude and ChatGPT) throughout the development of this project.

**Helpful suggestion:** When the Gemini API wasn't working due to quota and model availability issues, I was ready to abandon it and search for an entirely different API provider. Claude suggested simply trying a different Gemini model version (switching from gemini-2.0-flash to gemini-2.5-flash), which turned out to work immediately on the free tier. This saved significant time and kept the project on track instead of requiring me to learn a completely new API.

**Flawed suggestion:** Early in development, the AI suggested using default values in the query parser — for example, defaulting to "pop" as the genre when the user didn't specify one. I realized this was a bad design choice because it would bias every vague query toward pop music, even if the user had no preference for pop at all. I changed the parser to return None for unspecified fields instead, and updated the scoring logic to skip attributes that are None. This was my own design decision that improved the system's fairness and accuracy.