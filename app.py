import streamlit as st
import pandas as pd
import pickle
import requests

# Load movie data
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# OMDb API KEY
API_KEY = "615a7b65"

# Fetch poster using OMDb API
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'True':
            return data['Poster']
        else:
            return "https://via.placeholder.com/150x220?text=No+Image"

    except:
        return "https://via.placeholder.com/150x220?text=No+Image"


# Recommendation function
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]
    return movies[['title']].iloc[movie_indices]


# ---------------- UI ---------------- #

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):

    recommendations = get_recommendations(selected_movie)

    st.write("Top 10 recommended movies:")

    # 2 rows × 5 columns layout
    for i in range(0, 10, 5):
        cols = st.columns(5)

        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):

                movie_title = recommendations.iloc[j]['title']
                poster_url = fetch_poster(movie_title)

                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)