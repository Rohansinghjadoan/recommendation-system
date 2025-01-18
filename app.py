import pickle
import streamlit as st
import requests
import pandas as pd
import os





def fetch_poster(movie_id):
    try:
        api_key = os.getenv("TMDB_API_KEY", "2d204c7396e226dc1b437d650c03938a")  # Use environment variable
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# Recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error("Could not generate recommendations. Please try a different movie.")
        return [], []

# Streamlit App
st.header('🎬 Movie Recommender System')

# Load data
try:
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Required files not found. Please ensure 'movie_list.pkl' and 'similarity.pkl' are in the directory.")
    st.stop()

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names:
        columns = st.columns(5)
        for col, name, poster in zip(columns, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)


