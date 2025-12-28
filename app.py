import os
import pickle
import gdown
import streamlit as st
import pandas as pd
import requests

# Google Drive FILE IDs (correct)
ANIME_ID = "1zu_9DhcoG7qt_qnLErsaV7YdBkswwwBW"
SIM_ID = "1kfe3l1Kc-83PCBq2uPElcRW2Ej8RRri_"

ANIME_PATH = "anime.pkl"
SIM_PATH = "similarity.pkl"

def download_if_missing(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

download_if_missing(ANIME_ID, ANIME_PATH)
download_if_missing(SIM_ID, SIM_PATH)

# Load pickle files
anime_df = pickle.load(open(ANIME_PATH, "rb"))
similarity = pickle.load(open(SIM_PATH, "rb"))

anime_df['User Rating'] = pd.to_numeric(
    anime_df['User Rating'],
    errors='coerce'
)

#ADDing Bg
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



# Recommendation function
def recommend(anime_name):
    index = anime_df[anime_df['Title'] == anime_name].index[0]
    distances = similarity[index]

    anime_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return anime_list  # return index + score

import requests

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



# Streamlit UI
st.set_page_config(page_title="Anime Recommender", page_icon="🎌")
st.title("🎌 Anime Recommendation System")
st.write("Select an anime and get similar recommendations")

selected_anime = st.selectbox(
    "Choose an Anime",
    anime_df['Title'].values
)
st.set_page_config(page_title="Anime Recommender", page_icon="🎌")
add_bg_image(
    "https://images.unsplash.com/photo-1541560052-77ec1bbc09b3"
)



if st.button("Recommend"):
    recommendations = recommend(selected_anime)

    st.subheader("✨ Recommended Anime")

    cols = st.columns(len(recommendations))

    for col, (idx, _) in zip(cols, recommendations):
        with col:
            anime_title = anime_df.iloc[idx]['Title']
            rating = anime_df.iloc[idx]['User Rating']

            # 🎌 Fetch poster
            poster_url = fetch_anime_poster(anime_title)

            # 🖼️ Poster
            if poster_url:
                st.image(poster_url, width=160)
            else:
                st.write("No Image")

            # 🎌 Anime name
            st.markdown(
                f"<p style='text-align:center; font-weight:600'>"
                f"{anime_title}</p>",
                unsafe_allow_html=True
            )

            # ⭐ Rating
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
