# 🎵 Explainable AI Music Recommendation System

## Project Summary

This project builds an **Explainable AI Music Recommendation System** in Python. The system represents songs and a user taste profile as structured data, retrieves songs from a CSV catalog, applies a weighted scoring algorithm, ranks songs by how well they match the user's preferences, and returns the top K recommendations with clear explanations.

---

## Original Project (Modules 1–3)

This project is an extension of my earlier **Music Recommender Simulation (Module 3)**. The original system implemented a basic content-based recommendation algorithm that scored songs based on user preferences such as genre, mood, and energy.

In this final version, I expanded the system into a full applied AI pipeline by adding retrieval, explainability, guardrails, logging, and reliability testing to make the system more robust, transparent, and production-ready.

---

## Functionality

The system:

- Accepts user preferences such as genre, mood, energy, tempo, valence, danceability, and acoustic preference
- Retrieves songs from `data/songs.csv`
- Scores each song using a weighted content-based recommendation algorithm
- Ranks songs from strongest to weakest match
- Explains why each song was recommended
- Runs stress tests across different user profiles and edge cases
- Uses guardrails to validate inputs
- Logs system activity in `recommendation_log.txt`

---

## AI Features

### 1. Retrieval-Based Recommendation

The system uses a retrieval-based approach by loading a structured catalog of songs from `data/songs.csv`.

Each retrieved song is evaluated against the user profile using features such as:

- Genre  
- Mood  
- Energy  
- Tempo  
- Valence  
- Danceability  
- Acousticness  

The retrieved data directly affects the final recommendation output.

### 2. Reliability and Testing System

The system includes reliability testing through multiple user profiles and edge cases, including:

- Chill lofi listener  
- Deep intense rock listener  
- Conflicting energy vs mood preferences  
- Rare genre preference  
- Middle-of-the-road profile  

These tests help evaluate whether the recommender behaves consistently and reveal limitations in the scoring logic.

---

## Guardrails and Logging

### Guardrails

The system includes validation to prevent unsafe or incorrect behavior:

- Required user preference fields must be present  
- `target_energy` must be between 0 and 1  
- Optional numeric fields such as valence and danceability must be between 0 and 1  
- The system prevents recommendation generation if the song catalog is empty  
- Missing song data is handled with clear errors  

### Logging

The system logs important actions, including:

- Loading song data  
- Processing user preferences  
- Generating recommendations  
- Returning top results  

Logs are saved in:

```text
recommendation_log.txt