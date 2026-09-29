import streamlit as st
import pandas as pd
import pickle
import requests
import os

st.set_page_config(page_title="Movie Recommendation System", layout="wide", page_icon="🎬")

OMDB_API_KEY = "615a7b65"

# ── Load Model & Data ──
@st.cache_resource
def load_movie_artifacts():
    # 1. Preferred lightweight precomputed dict
    if os.path.exists("recommendations_dict.pkl") and os.path.exists("movies_list.pkl"):
        with open("movies_list.pkl", "rb") as f:
            movies_df = pickle.load(f)
        with open("recommendations_dict.pkl", "rb") as f:
            rec_dict = pickle.load(f)
        return movies_df, rec_dict, None

    # 2. Local full pickle if available
    if os.path.exists("movie_data.pkl"):
        with open("movie_data.pkl", "rb") as f:
            movies_df, cosine_sim = pickle.load(f)
        return movies_df, None, cosine_sim

    # 3. Fallback: On-the-fly computation from CSV
    if os.path.exists("tmdb_5000_movies.csv"):
        df = pd.read_csv("tmdb_5000_movies.csv")
        df['overview'] = df['overview'].fillna('')
        df['title'] = df['title'].fillna('')
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        tfidf = TfidfVectorizer(stop_words='english', max_features=3000)
        tfidf_mat = tfidf.fit_transform(df['overview'])
        sim_mat = cosine_similarity(tfidf_mat, tfidf_mat)
        return df[['id', 'title']], None, sim_mat

    raise FileNotFoundError("Could not find movie data or model artifacts.")

movies, rec_dict, cosine_sim = load_movie_artifacts()

# ── Poster Fetcher with Caching ──
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_poster(movie_title):
    try:
        url = f"https://www.omdbapi.com/?t={requests.utils.quote(movie_title)}&apikey={OMDB_API_KEY}"
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("Response") == "True" and data.get("Poster") and data.get("Poster") != "N/A":
                return data["Poster"]
    except Exception:
        pass
    return "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&auto=format&fit=crop&q=60"

# ── Recommendation Function ──
def get_recommendations(selected_title, num_recs=5):
    if rec_dict and selected_title in rec_dict:
        return rec_dict[selected_title][:num_recs]
    elif cosine_sim is not None:
        idx_series = movies[movies['title'] == selected_title]
        if idx_series.empty:
            return []
        idx = idx_series.index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]
        indices = [i[0] for i in sim_scores]
        return movies['title'].iloc[indices].tolist()
    return []

# ── UI Layout ──
st.title("🎬 Movie Recommendation System")
st.markdown("Content-Based Filtering Recommendation Engine using **Cosine Similarity & TF-IDF NLP**.")

col_select, col_count = st.columns([3, 1])

with col_select:
    all_titles = sorted(movies['title'].dropna().unique().tolist())
    selected_movie = st.selectbox(
        "Search or Select a Movie:",
        all_titles,
        index=all_titles.index("Avatar") if "Avatar" in all_titles else 0
    )

with col_count:
    rec_count = st.slider("Recommendations Count", min_value=5, max_value=10, value=5)

if st.button("🚀 Get Recommendations", use_container_width=True, type="primary"):
    with st.spinner("Finding similar movies and fetching official posters..."):
        recs = get_recommendations(selected_movie, num_recs=rec_count)
        
    if not recs:
        st.warning("No recommendations found for this title.")
    else:
        st.subheader(f"✨ Movies Similar to '{selected_movie}':")
        cols = st.columns(len(recs))
        for col, movie_name in zip(cols, recs):
            poster_url = fetch_poster(movie_name)
            with col:
                st.image(poster_url, use_container_width=True)
                st.caption(f"**{movie_name}**")

st.divider()
with st.expander("ℹ️ About This Recommendation Engine"):
    st.write("""
    - **Algorithm:** Content-Based Filtering with Cosine Similarity.
    - **Vector Space:** Natural Language Processing (NLP) with TF-IDF Vectorization over plot overviews, genres, and keywords.
    - **Metadata & Artwork:** Dynamic integration with OMDb REST API for real-time movie cover art.
    - **Developer:** Laxmi Sahu ([GitHub](https://github.com/laxmi345))
    """)