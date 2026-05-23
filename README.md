# 🎬 Movie Recommendation System

A **content-based movie recommendation engine** built with Python and deployed as an interactive web app using Streamlit. Select any movie from 5000+ titles and instantly get 10 similar recommendations with posters.

---

## 📸 What It Does

- Select a movie from a dropdown of **4800+ Hollywood films**
- Click **"Recommend"** → get **Top 10 similar movies**
- Each result shows the **movie poster** (fetched live via OMDb API) and title
- Results displayed in a clean **2 rows × 5 columns** grid layout

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Pandas** | Data loading, cleaning, merging |
| **NumPy** | Numerical operations |
| **Scikit-learn** | TF-IDF Vectorizer + Cosine Similarity |
| **Streamlit** | Web app UI |
| **Pickle** | Save/load model data |
| **Requests** | HTTP calls to OMDb API |
| **OMDb API** | Fetch live movie posters |
| **Jupyter Notebook** | Data exploration & model building |
| **ast module** | Parse JSON-like strings in CSV |

---

## 📁 Project Structure

```
movie-recommendation-system/
│
├── movie_recommendation.ipynb   # Data preprocessing + model building
├── app.py                       # Streamlit web application
├── requirements.txt             # Python dependencies
├── movie_data.pkl               # Saved model (movies df + cosine_sim matrix)
│
└── data/
    ├── tmdb_5000_movies.csv
    └── tmdb_5000_credits.csv
```

---

## ⚙️ How It Works — Step by Step

### Step 1: Load Data
Two CSV files from the TMDB 5000 dataset:
- `tmdb_5000_movies.csv` → movie details (overview, genres, keywords)
- `tmdb_5000_credits.csv` → cast and crew info

### Step 2: Merge & Clean
```python
movies = movies.merge(credits, left_on='id', right_on='movie_id')
movies = movies[['id', 'title_x', 'overview', 'genres', 'keywords', 'cast', 'crew']]
```

### Step 3: Parse JSON Columns
Genres, keywords, and cast were stored as JSON strings. Extracted just the names:
```python
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

movies['genres']   = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast']     = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)[:3]])
```

### Step 4: Extract Director
```python
def extract_director(text):
    data = ast.literal_eval(text)
    return [i['name'] for i in data if i['job'] == 'Director']
```

### Step 5: Build Tags Column ⭐ (Core Feature)
Combined all features into one text string per movie:
```python
movies['tags'] = overview + genres + keywords + cast + director
```
Example for *Avatar*:
> `"a paraplegic marine dispatched to the moon pandora action adventure fantasy sam worthington zoe saldana james cameron"`

### Step 6: TF-IDF Vectorization
```python
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['tags'])
```
Converts text into numerical vectors. Removes common words like "the", "is", "a".

### Step 7: Cosine Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
```
Creates a **4800 × 4800 matrix** — every movie's similarity score against every other movie. Score ranges from 0 (no similarity) to 1 (identical).

### Step 8: Save with Pickle
```python
import pickle
with open('movie_data.pkl', 'wb') as file:
    pickle.dump((movies, cosine_sim), file)
```

### Step 9: Streamlit App
```python
def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:11]
    return movies['title'].iloc[[i[0] for i in sim_scores]]
```

---

## 📦 Requirements

```
streamlit
pandas
requests
scikit-learn
```

---

## 📊 Dataset

**TMDB 5000 Movie Dataset** from Kaggle
- `tmdb_5000_movies.csv` — 4803 movies with budget, genres, keywords, overview, popularity, etc.
- `tmdb_5000_credits.csv` — Cast and crew details for each movie

---

## 💡 How Recommendations Work

This is a **Content-Based Filtering** system — it recommends movies similar in *content* to what you selected, not based on what other users watched.

```
User selects "The Dark Knight"
        ↓
Find its index in the movies dataframe
        ↓
Look up its row in the cosine_sim matrix
        ↓
Sort all other movies by similarity score (highest first)
        ↓
Return top 10 (skip index 0 — that's the movie itself)
        ↓
Fetch posters from OMDb API → Display in grid
```

---

## ✅ Strengths

- Works without any user login or rating history
- Handles 4800+ movies efficiently
- Flexible tag-based approach captures genre, cast, director, and plot
- Live poster fetching makes UI visually rich
- Lightweight — runs on any machine with Python

---

## ⚠️ Limitations

- No personalization — same input always gives same output
- TF-IDF doesn't understand word meaning (e.g., "action" ≠ "thriller")
- Poster quality depends on OMDb API availability
- Recommendations only as good as the tags — missing data = weaker results

---

## 🔮 Future Improvements

- Add **Collaborative Filtering** using user ratings
- Use **Word2Vec or BERT embeddings** instead of TF-IDF for semantic understanding
- Add **genre/year filters** in the UI
- Deploy on **Streamlit Cloud** or **Hugging Face Spaces**

---

## 👩‍💻 Author

**Laxmi Sahu**
B.Tech Data Science — Gyan Ganga Institute of Technology & Sciences, Jabalpur
- GitHub: [github.com/laxmi345](https://github.com/laxmi345)
- LinkedIn: [linkedin.com/in/laxmi-sahu-728790321](https://linkedin.com/in/laxmi-sahu-728790321)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
