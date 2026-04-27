import csv
import logging
from typing import List, Dict, Tuple

logging.basicConfig(
    filename="recommendation_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

REQUIRED_FIELDS = ["favorite_genre", "favorite_mood", "target_energy", "likes_acoustic"]


def validate_user_prefs(user_prefs: Dict) -> None:
    """Validate user preferences before scoring songs."""
    for field in REQUIRED_FIELDS:
        if field not in user_prefs:
            raise ValueError(f"Missing required user preference: {field}")

    if not 0 <= user_prefs["target_energy"] <= 1:
        raise ValueError("target_energy must be between 0 and 1.")

    for optional_field in ["preferred_valence", "preferred_danceability"]:
        if optional_field in user_prefs and user_prefs[optional_field] is not None:
            if not 0 <= user_prefs[optional_field] <= 1:
                raise ValueError(f"{optional_field} must be between 0 and 1.")


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file and return a list of song dictionaries."""
    songs: List[Dict] = []

    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                song = {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"].lower().strip(),
                    "mood": row["mood"].lower().strip(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
                songs.append(song)

        if not songs:
            raise ValueError("Song catalog is empty.")

        logging.info("Loaded %s songs from %s", len(songs), csv_path)
        return songs

    except FileNotFoundError:
        logging.error("Song file not found: %s", csv_path)
        raise FileNotFoundError(f"Song file not found at path: {csv_path}")


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return score plus explanation reasons."""
    score = 0.0
    reasons = []

    favorite_genre = user_prefs["favorite_genre"].lower().strip()
    favorite_mood = user_prefs["favorite_mood"].lower().strip()

    if song["genre"] == favorite_genre:
        score += 24
        reasons.append(f"Genre match ({song['genre']}): +24 pts")
    else:
        reasons.append(f"No genre match ({song['genre']} vs {favorite_genre}): +0 pts")

    if song["mood"] == favorite_mood:
        score += 16
        reasons.append(f"Mood match ({song['mood']}): +16 pts")
    else:
        reasons.append(f"No mood match ({song['mood']} vs {favorite_mood}): +0 pts")

    target_energy = user_prefs["target_energy"]
    energy_proximity = 1 - abs(target_energy - song["energy"])
    energy_points = 24 * max(0.0, energy_proximity)
    score += energy_points
    reasons.append(f"Energy closeness: +{energy_points:.1f} pts")

    acoustic_target = 1.0 if user_prefs["likes_acoustic"] else 0.0
    acoustic_proximity = 1 - abs(acoustic_target - song["acousticness"])
    acoustic_points = 16 * max(0.0, acoustic_proximity)
    score += acoustic_points
    reasons.append(f"Acoustic fit: +{acoustic_points:.1f} pts")

    if user_prefs.get("preferred_tempo_bpm") is not None:
        tempo_proximity = 1 - abs(user_prefs["preferred_tempo_bpm"] - song["tempo_bpm"]) / 120
        tempo_points = 8 * max(0.0, tempo_proximity)
        score += tempo_points
        reasons.append(f"Tempo closeness: +{tempo_points:.1f} pts")

    if user_prefs.get("preferred_valence") is not None:
        valence_proximity = 1 - abs(user_prefs["preferred_valence"] - song["valence"])
        valence_points = 6 * max(0.0, valence_proximity)
        score += valence_points
        reasons.append(f"Valence closeness: +{valence_points:.1f} pts")

    if user_prefs.get("preferred_danceability") is not None:
        dance_proximity = 1 - abs(user_prefs["preferred_danceability"] - song["danceability"])
        dance_points = 6 * max(0.0, dance_proximity)
        score += dance_points
        reasons.append(f"Danceability closeness: +{dance_points:.1f} pts")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Validate input, score songs, rank results, and return top recommendations."""
    validate_user_prefs(user_prefs)

    if not songs:
        raise ValueError("No songs available for recommendation.")

    logging.info("Generating recommendations for user preferences: %s", user_prefs)

    results: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))

    ranked_results = sorted(results, key=lambda item: item[1], reverse=True)
    top_results = ranked_results[:k]

    logging.info("Returned %s recommendations from %s songs", len(top_results), len(songs))

    return top_results