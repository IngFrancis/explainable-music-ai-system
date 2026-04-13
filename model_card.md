# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a content-based music recommender designed to suggest
songs from a small catalog based on a user's stated taste preferences.
It generates a ranked list of up to 5 song recommendations along with
an explanation of why each song was selected.

The system assumes the user can describe their preferences upfront —
favorite genre, mood, energy level, and whether they like acoustic music.
It does not learn from listening history or adapt over time. This is a
classroom simulation built for educational exploration, not for real
users or production deployment.

---

## 3. How the Model Works

VibeFinder works by giving every song in the catalog a score based on
how closely it matches what the user said they want. Think of it like
a judge at a competition — each song gets points in several categories,
and the songs with the most points win a spot in the recommendation list.

The judge awards points for things like whether the song's genre matches
the user's favorite, whether the mood fits, how close the energy level
is to what the user prefers, and whether the song feels acoustic or
electronic. Some categories are worth more points than others — genre
and energy are the most important, followed by mood and acoustic feel.
Optional preferences like tempo, positivity, and danceability add bonus
points when provided.

Once every song has a score, the list is sorted from highest to lowest
and the top five are returned as recommendations, each with a breakdown
explaining exactly where its points came from.

---

## 4. Data

The catalog contains 18 songs stored in a CSV file. Each song has ten
attributes: a unique ID, title, artist, genre, mood, energy, tempo,
valence, danceability, and acousticness.

The catalog covers 14 genres including pop, lofi, rock, ambient, jazz,
synthwave, indie pop, classical, metal, r&b, electronic, country, latin,
and hip hop. Moods represented include happy, chill, intense, relaxed,
moody, focused, romantic, angry, nostalgic, energetic, and melancholic.

The original starter file had 10 songs. Eight additional songs were
generated using Copilot to fill gaps in genre and mood coverage. Despite
this expansion, the catalog still skews toward certain genres — lofi has
3 songs, pop and classical have 2 each, and every other genre has exactly
one. Musical taste dimensions like lyrics, language, cultural context,
tempo ranges, and live vs studio recordings are not represented at all.

---

## 5. Strengths

The system works best for users whose preferred genre and mood appear
multiple times in the catalog. Lofi and chill listeners in particular
receive strong, well-differentiated recommendations — Library Rain and
Midnight Coding both scored above 93 for a chill lofi profile, showing
the scoring logic can clearly separate good matches from poor ones when
the data supports it.

The scoring also captures the intuitive idea that closeness matters more
than absolute values. A song with energy 0.72 correctly ranks above one
with energy 0.30 for a user who prefers 0.70, because the system rewards
proximity rather than just high or low values. The reasons list makes
the logic fully transparent, which is a meaningful strength for a
simulation meant to teach how recommenders work.

---

## 6. Limitations and Bias

This recommender has several structural biases discovered during testing
and confirmed through Copilot's analysis.

First, the catalog is heavily uneven across genres — lofi has 3 songs,
pop and classical have 2 each, and every other genre has exactly 1. Since
genre matching is worth 24 points, users who prefer single-song genres like
metal, latin, or hip hop receive one strong recommendation followed by four
irrelevant results. There are simply no backup options in those genres.

Second, the likes_acoustic boolean creates strong genre-level pressure
because acousticness is genre-clustered in the catalog. Setting
likes_acoustic=True systematically boosts classical, ambient, jazz, and
lofi while suppressing metal, rock, electronic, and hip hop — regardless
of whether the user actually wants those genres. A float preference (0.0
to 1.0) would be more fair than a binary True/False toggle.

Third, low-energy users who dislike acoustic sound are indirectly
disadvantaged. Most low-energy songs in the catalog are also highly
acoustic, so a user with target_energy=0.2 and likes_acoustic=False
gets penalized on both energy and acoustic fit simultaneously — not
because the formula is unfair, but because the data is correlated in
that direction.

Fourth, certain genre and mood combinations simply do not exist in the
catalog — for example metal+chill, hip hop+happy, or classical+energetic.
Users with those preferences can never achieve a full categorical score,
making the system structurally incapable of serving them well regardless
of how good their numeric feature matches are.

Fifth, the OOP Recommender.recommend() method currently returns the first
k songs from the list without scoring them at all. If this path is ever
used instead of recommend_songs(), recommendations would reflect CSV row
order rather than actual user preferences — a silent but serious bug.

---

## 7. Evaluation

Six user profiles were tested against the full 18-song catalog: three
standard profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and
three adversarial edge cases (Conflicting Energy vs Mood, Rare Genre
Metal, Middle-of-the-Road).

For each profile the top 5 results were reviewed and compared against
musical intuition. The Chill Lofi and Deep Intense Rock profiles produced
results that felt accurate — the correct songs ranked first with large
score gaps separating them from the rest. The most surprising finding
was that Gym Hero by Max Pulse appeared in the top 3 of four different
profiles despite being a pop song, because its extreme energy and low
acousticness earned 35+ points before genre and mood were even checked.

A feature removal experiment was also run — the mood scoring was
temporarily disabled to observe how rankings shifted. The results
confirmed that mood was doing meaningful work: removing it caused
deserving songs to drop unfairly and flattened the score distribution,
making recommendations harder to differentiate.

---

## 8. Future Work

The most impactful improvement would be expanding the catalog
significantly — at least 5 songs per genre would give the system enough
variety to make meaningful recommendations for all user types, not just
the few genres with multiple entries.

Replacing the likes_acoustic boolean with a float preference (0.0 to 1.0)
would also improve fairness by allowing partial acoustic preference rather
than an all-or-nothing toggle. Similarly, replacing exact genre matching
with partial credit for related genres (for example awarding 12 points
for indie pop when the user prefers pop) would reduce the harsh penalty
for near-miss genre matches.

Adding a diversity rule to the ranking step — for example ensuring no
single artist appears more than once in the top 5 — would prevent the
system from clustering too tightly around one part of the catalog.
Finally, implementing the OOP Recommender.recommend() method with actual
scoring logic would fix the silent bug identified during evaluation.

---

## 9. Personal Reflection

Building this project made it clear that recommendation systems are not
just about math — they are deeply shaped by the data they run on. The
scoring formula itself was symmetric and fair, but the catalog's uneven
genre distribution meant some users were structurally disadvantaged
before a single score was calculated. That was unexpected and eye-opening.

The experiment of removing mood from the scoring was also revealing. It
showed that even a feature worth only 16 points out of 100 can be the
difference between recommendations that feel right and ones that feel
generic. Every weight is a design decision with real consequences for
real listeners, and small changes can quietly change who the system
serves well and who it ignores.
