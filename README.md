# 🎵 Music Recommender Simulation

## Project Summary

This project builds a small content-based music recommender system in Python.
The system represents songs and a user taste profile as data, applies a
weighted scoring algorithm to rank songs by how well they match the user's
preferences, and returns the top K recommendations with explanations.

---

## How The System Works

Music platforms like Spotify don't just recommend songs at random — they
study patterns. Collaborative filtering picks up on what people with similar
taste are listening to, so if someone who likes everything you like also
loves a new song, there's a good chance you will too. Content-based
filtering takes a different angle: it looks at the song itself — how fast
it is, how intense, how happy it sounds — and finds other tracks with a
similar feel. Spotify blends both ideas together so recommendations feel
both personally familiar and occasionally surprising.

My version focuses on content-based filtering. When a user sets their
preferences, the system scores every song by measuring how close each
feature is to what the user actually wants — not just what's highest or
lowest, but what's closest. Those feature scores get combined using weights,
since things like energy tend to matter more than mood when defining a vibe.
The scoring rule handles one song at a time, and the ranking rule takes all
those scores and builds the final recommendation list from best match down.

---

### Song Object Features

- `genre` — style category (pop, rock, lofi, etc.)
- `mood` — emotional vibe (happy, chill, intense, etc.)
- `energy` — intensity level (0 to 1)
- `tempo_bpm` — speed in beats per minute
- `valence` — positivity of feel (0 to 1)
- `danceability` — rhythmic suitability (0 to 1)
- `acousticness` — acoustic vs electronic texture (0 to 1)

### UserProfile Object Features

- `favorite_genre` — favorite style category
- `favorite_mood` — current or general mood preference
- `target_energy` — ideal intensity level (0 to 1)
- `likes_acoustic` — prefers acoustic sound (True/False)
- `preferred_tempo_bpm` — ideal song speed (optional)
- `preferred_valence` — emotional positivity preference (optional)
- `preferred_danceability` — groove preference (optional)

---

### Algorithm Recipe (Scoring Weights)

Each song is scored out of a maximum of 100 points:

| Feature                | Points | Method                                                            |
| ---------------------- | ------ | ----------------------------------------------------------------- |
| Genre match            | 24 pts | +24 if song genre equals user's favorite genre, else 0            |
| Energy closeness       | 24 pts | `1 - abs(target_energy - song.energy)` × 24                       |
| Mood match             | 16 pts | +16 if song mood equals user's favorite mood, else 0              |
| Acoustic fit           | 16 pts | converts `likes_acoustic` bool to 0.0 or 1.0, then proximity × 16 |
| Tempo closeness        | 8 pts  | `1 - abs(target_tempo - song.tempo) / 120` × 8 (optional)         |
| Valence closeness      | 6 pts  | `1 - abs(target_valence - song.valence)` × 6 (optional)           |
| Danceability closeness | 6 pts  | `1 - abs(target_dance - song.danceability)` × 6 (optional)        |

Optional fields score 0 if not provided, keeping comparisons fair across profiles.

---

### Flowchart

```mermaid
flowchart TD
    A[Input user preferences<br/>favorite_genre, favorite_mood, target_energy, likes_acoustic<br/>optional: preferred_tempo_bpm, preferred_valence, preferred_danceability] --> B[Load song catalog CSV]
    B --> C[Initialize empty scored_results list]
    C --> D{{More songs to score?}}
    D -- Yes --> E[Get next song]
    E --> F[Run score_song(user, song)]
    F --> G[Genre match check<br/>0 or +24]
    G --> H[Mood match check<br/>0 or +16]
    H --> I[Energy proximity<br/>+0 to +24]
    I --> J[Acoustic fit<br/>+0 to +16]
    J --> K{Optional preferences present?}
    K -- Yes --> L[Tempo +0 to +8, Valence +0 to +6, Danceability +0 to +6]
    K -- No --> M[Skip optional scoring]
    L --> N[Calculate total score and reasons]
    M --> N
    N --> O[Append song, score, reasons to scored_results]
    O --> D
    D -- No --> P[Sort scored_results by score descending]
    P --> Q[Select top K songs]
    Q --> R[Output: song + score + reasons]
```

---

### Known Limitations and Potential Biases

- **Genre over-prioritization:** Genre carries 24 points but the catalog
  only has 1–2 songs per genre. A genre match might score a mediocre song
  higher than a near-perfect energy and mood match in a different genre.

- **Cold start problem:** This system requires the user to manually set
  preferences. New users with no listening history get no personalization
  benefit until they fill out their profile.

- **Mood is session-dependent:** A user's favorite mood might be "chill"
  overall but "intense" during a workout. The current profile doesn't
  account for context or time of day.

- **likes_acoustic is too blunt:** A boolean True/False loses nuance — a
  user might enjoy slightly acoustic songs but not fully acoustic ones. A
  float preference would be more accurate.

- **Small catalog:** With only 18 songs, top K results may include poor
  matches simply because there aren't enough songs to fill the list.

---

## Sample Terminal Output

```
========================================================================
MUSIC RECOMMENDATIONS
========================================================================
User Preferences:
  Genre: pop
  Mood: happy
  Target Energy: 0.8
  Likes Acoustic: False
  Preferred Tempo BPM: 120
  Preferred Valence: 0.78
  Preferred Danceability: 0.8
========================================================================
Rank #1
Song: Sunrise City — Neon Echo
Final Score: 96.09/100
Reasons:
  - Genre match (pop): +24 pts
  - Mood match (happy): +16 pts
  - Energy closeness: +23.5 pts
  - Acoustic fit: +13.1 pts
  - Tempo closeness: +7.9 pts
  - Valence closeness: +5.6 pts
  - Danceability closeness: +5.9 pts
------------------------------------------------------------------------
Rank #2
Song: Gym Hero — Max Pulse
Final Score: 78.74/100
Reasons:
  - Genre match (pop): +24 pts
  - No mood match (intense vs happy): +0 pts
  - Energy closeness: +20.9 pts
  - Acoustic fit: +15.2 pts
  - Tempo closeness: +7.2 pts
  - Valence closeness: +5.9 pts
  - Danceability closeness: +5.5 pts
------------------------------------------------------------------------
Rank #3
Song: Rooftop Lights — Indigo Parade
Final Score: 68.87/100
Reasons:
  - No genre match (indie pop vs pop): +0 pts
  - Mood match (happy): +16 pts
  - Energy closeness: +23.0 pts
  - Acoustic fit: +10.4 pts
  - Tempo closeness: +7.7 pts
  - Valence closeness: +5.8 pts
  - Danceability closeness: +5.9 pts
------------------------------------------------------------------------
Rank #4
Song: City Cipher — Metro Mode
Final Score: 54.98/100
Reasons:
  - No genre match (hip hop vs pop): +0 pts
  - No mood match (energetic vs happy): +0 pts
  - Energy closeness: +23.8 pts
  - Acoustic fit: +14.6 pts
  - Tempo closeness: +6.4 pts
  - Valence closeness: +5.0 pts
  - Danceability closeness: +5.2 pts
------------------------------------------------------------------------
Rank #5
Song: Sunset Barrio — Sol Fuego
Final Score: 53.75/100
Reasons:
  - No genre match (latin vs pop): +0 pts
  - No mood match (romantic vs happy): +0 pts
  - Energy closeness: +21.8 pts
  - Acoustic fit: +12.6 pts
  - Tempo closeness: +7.9 pts
  - Valence closeness: +5.8 pts
  - Danceability closeness: +5.6 pts
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

---

## Stress Test: Diverse User Profiles

### Profile 1: High-Energy Pop

```
========================================================================
PROFILE: High-Energy Pop
========================================================================
User Preferences:
  favorite_genre: pop
  favorite_mood: happy
  target_energy: 0.9
  likes_acoustic: False
  preferred_tempo_bpm: 130
  preferred_valence: 0.85
  preferred_danceability: 0.88
========================================================================
Rank #1 — Sunrise City — Neon Echo — 93.80/100
Rank #2 — Gym Hero — Max Pulse — 81.87/100
Rank #3 — Rooftop Lights — Indigo Parade — 66.04/100
Rank #4 — Neon Circuit — Pulse Harbor — 54.81/100
Rank #5 — City Cipher — Metro Mode — 53.31/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Genre + mood match drives the top 2 spots. Songs with only
one matching category (genre or mood) still rank above pure energy matches.

---

### Profile 2: Chill Lofi

```
========================================================================
PROFILE: Chill Lofi
========================================================================
User Preferences:
  favorite_genre: lofi
  favorite_mood: chill
  target_energy: 0.38
  likes_acoustic: True
  preferred_tempo_bpm: 75
  preferred_valence: 0.58
  preferred_danceability: 0.6
========================================================================
Rank #1 — Library Rain — Paper Lanterns — 96.60/100
Rank #2 — Midnight Coding — LoRoom — 93.96/100
Rank #3 — Focus Flow — LoRoom — 79.61/100
Rank #4 — Spacewalk Thoughts — Orbit Bloom — 69.76/100
Rank #5 — Coffee Shop Stories — Slow Stereo — 55.86/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Two lofi songs scored 93–96, showing strong separation when
the catalog has multiple songs matching genre and mood. Ambient sneaks into
rank 4 via mood match alone.

---

### Profile 3: Deep Intense Rock

```
========================================================================
PROFILE: Deep Intense Rock
========================================================================
User Preferences:
  favorite_genre: rock
  favorite_mood: intense
  target_energy: 0.92
  likes_acoustic: False
  preferred_tempo_bpm: 155
  preferred_valence: 0.45
  preferred_danceability: 0.65
========================================================================
Rank #1 — Storm Runner — Voltline — 97.72/100
Rank #2 — Gym Hero — Max Pulse — 70.13/100
Rank #3 — Iron Pulse — Black Forge — 56.45/100
Rank #4 — Neon Circuit — Pulse Harbor — 53.69/100
Rank #5 — City Cipher — Metro Mode — 52.01/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Storm Runner scored nearly perfectly. The 27-point gap between
rank 1 and rank 2 shows how dominant a full genre + mood + energy match is.

---

### Edge Case 1: Conflicting Energy vs Mood

```
========================================================================
PROFILE: Edge Case: Conflicting Energy vs Mood
========================================================================
User Preferences:
  favorite_genre: classical
  favorite_mood: melancholic
  target_energy: 0.95
  likes_acoustic: True
  preferred_valence: 0.1
========================================================================
Rank #1 — Velvet Strings — Aurora Quartet — 48.24/100
Rank #2 — Old Film Memory — Atlas Reed — 47.74/100
Rank #3 — Backroad Moon — Willow Ridge — 40.16/100
Rank #4 — Iron Pulse — Black Forge — 29.14/100
Rank #5 — Storm Runner — Voltline — 28.36/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Max score was only 48.24/100 — the conflicting preferences
(high energy + acoustic + melancholic) could not be satisfied simultaneously.
The system still returned results but with low confidence scores, exposing
a key weakness when user preferences contradict each other.

---

### Edge Case 2: Rare Genre (Metal)

```
========================================================================
PROFILE: Edge Case: Rare Genre (Metal)
========================================================================
User Preferences:
  favorite_genre: metal
  favorite_mood: angry
  target_energy: 0.96
  likes_acoustic: False
  preferred_tempo_bpm: 168
  preferred_valence: 0.31
  preferred_danceability: 0.61
========================================================================
Rank #1 — Iron Pulse — Black Forge — 99.36/100
Rank #2 — Storm Runner — Voltline — 54.81/100
Rank #3 — Gym Hero — Max Pulse — 51.70/100
Rank #4 — Neon Circuit — Pulse Harbor — 50.78/100
Rank #5 — City Cipher — Metro Mode — 49.10/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Iron Pulse scored 99.36 but ranks 2–5 dropped to ~50.
With only one metal song in the catalog there are no backup options.
This confirms the small catalog limitation — the system has nowhere to go
after the one perfect match.

---

### Edge Case 3: Middle-of-the-Road

```
========================================================================
PROFILE: Edge Case: Middle-of-the-Road
========================================================================
User Preferences:
  favorite_genre: jazz
  favorite_mood: focused
  target_energy: 0.5
  likes_acoustic: True
  preferred_tempo_bpm: 100
  preferred_valence: 0.5
  preferred_danceability: 0.5
========================================================================
Rank #1 — Coffee Shop Stories — Slow Stereo — 76.95/100
Rank #2 — Focus Flow — LoRoom — 67.61/100
Rank #3 — Library Rain — Paper Lanterns — 51.21/100
Rank #4 — Midnight Coding — LoRoom — 50.89/100
Rank #5 — Backroad Moon — Willow Ridge — 50.35/100
------------------------------------------------------------------------
Summary: evaluated 18 songs, returned top 5.
```

**Finding:** Scores clustered between 50–76 with no strong separation.
Middle-of-the-road preferences produce mediocre recommendations for
everyone rather than great recommendations for anyone. Ranks 3–5 are
nearly tied, making the ordering unreliable.

---

## Experiments You Tried

### Observation: Gym Hero appears in 4 out of 6 profiles

Gym Hero by Max Pulse ranked in the top 3 for High-Energy Pop, Deep Intense
Rock, Rare Genre Metal, and Middle-of-the-Road profiles despite being a pop
song. Investigation showed that its combination of very high energy (0.93)
and very low acousticness (0.05) earns 35+ points before genre and mood are
checked. With only 18 songs in the catalog, few other songs compete on both
dimensions simultaneously.

**Root cause:** Energy and acoustic fit together carry 40 points — the same
as genre and mood combined. A song that scores perfectly on both numeric
features can outrank genre and mood mismatches, which may not reflect real
listening preferences.

**Three fixes Copilot suggested:**

1. Increase mood weight from 16 to 24 pts so mood differentiates profiles
   more strongly (e.g. pop vs rock users get different results)

2. Add partial genre credit — non-matching genre scores 8 pts instead of 0,
   reducing the all-or-nothing penalty and increasing variety

3. Add a diversity penalty — reduce score by 10% for songs that appear
   repeatedly across recommendations, forcing more variety

**What I tried:** Temporarily increased mood weight from 16 to 24 and
reduced energy from 24 to 16. Gym Hero dropped out of the rock and metal
profiles since its mood (intense) no longer compensated for the genre
mismatch as easily. Reverted back to original weights to keep tests stable.

---

## Limitations and Risks

- It only works on a small 18-song catalog
- It does not understand lyrics or song meaning
- It may over-favor genre matches over better overall vibe matches
- It treats all users as having a single fixed taste profile

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- About how recommenders turn data into predictions
- About where bias or unfairness could show up in systems like this
