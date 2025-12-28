import pickle
import streamlit as st
import pandas as pd
import requests

# MUST be first Streamlit command
st.set_page_config(
    page_title="Anime Recommender",
    page_icon="🎌",
    layout="wide"
)

# Load models directly from repo
anime_df = pickle.load(open("anime.pkl", "rb"))
top_k_sim = pickle.load(open("top_k_similarity.pkl", "rb"))

anime_df["User Rating"] = pd.to_numeric(
    anime_df["User Rating"], errors="coerce"
)

def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def recommend(anime_name):
    index = anime_df[anime_df["Title"] == anime_name].index[0]
    return [(int(i), float(s)) for i, s in top_k_sim[index][:5]]

@st.cache_data(show_spinner=False)
def fetch_anime_poster(anime_name):
    url = "https://api.jikan.moe/v4/anime"
    params = {"q": anime_name, "limit": 1}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return data["data"][0]["images"]["jpg"]["image_url"]
    except:
        return None

# UI
st.title("🎌 Anime Recommendation System")
st.write("Select an anime and get similar recommendations")

add_bg_image(
    "https://images.unsplash.com/photo-1541560052-77ec1bbc09b3"
)

selected_anime = st.selectbox(
    "Choose an Anime",
    anime_df["Title"].values
)

if st.button("Recommend"):
    recommendations = recommend(selected_anime)

    st.subheader("✨ Recommended Anime")
    cols = st.columns(len(recommendations))

    for col, (idx, score) in zip(cols, recommendations):
        with col:
            anime_title = anime_df.iloc[idx]["Title"]
            rating = anime_df.iloc[idx]["User Rating"]

            poster_url = fetch_anime_poster(anime_title)
            if poster_url:
                st.image(poster_url, width=160)

            st.markdown(
                f"<p style='text-align:center; font-weight:600'>{anime_title}</p>",
                unsafe_allow_html=True
            )

            if not pd.isna(rating):
                st.markdown(
                    f"<p style='text-align:center'>⭐ {rating:.1f}</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<p style='text-align:center'>⭐ N/A</p>",
                    unsafe_allow_html=True
                )

