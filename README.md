# 🎬 Movie Recommendation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://laxmi-movie-recommend.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, interactive **Content-Based Movie Recommendation Engine** that recommends movies based on metadata similarity (plot summaries, genres, keywords, and cast) powered by **Natural Language Processing (NLP)** and **Cosine Similarity**.

---

## 🚀 Key Features

* **🧠 Content-Based Filtering:** Utilizes TF-IDF and Cosine Similarity to find mathematically nearest neighbor films across 4,800+ titles.
* **🖼️ Dynamic Artwork Fetching:** Integrated with the **OMDb API** to dynamically fetch high-resolution posters and artwork for each recommended title.
* **⚡ Ultra-Fast In-Memory Engine:** Pre-vectorized similarity models compressed to sub-megabyte footprint for instant recommendations.
* **🎛️ Interactive Streamlit UI:** Search and select dropdown, dynamic recommendation count sliders, and responsive grid layout.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **NLP & Machine Learning:** [Scikit-Learn](https://scikit-learn.org/) (TF-IDF Vectorizer, Cosine Similarity)
* **Data Manipulation:** Pandas, NumPy
* **External APIs:** OMDb REST API

---

## 💻 Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/laxmi345/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Live Interactive App

👉 **Live Demo:** [laxmi-movie-recommend.streamlit.app](https://laxmi-movie-recommend.streamlit.app/)

## 🌐 Deploy to Streamlit Community Cloud (Free)

1. Sign in to [share.streamlit.io](https://share.streamlit.io/) with your GitHub account.
2. Click **"New App"**.
3. Select repository: `laxmi345/movie-recommendation-system`.
4. Main file path: `app.py`.
5. Click **"Deploy!"**.

---

## 👤 Author
* **Developer:** Laxmi Sahu ([@laxmi345](https://github.com/laxmi345))
* **Portfolio:** [portfolio-laxmisahu.vercel.app](https://portfolio-laxmisahu.vercel.app/)