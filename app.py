import streamlit as st
import pickle

# Load data
movies = pickle.load(open("movie_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Streamlit UI
st.header("Movie Recommender System")
selected_movie = st.selectbox("Choose a movie:", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movies = []
    for i in distances[1:6]:  # Top 5 similar movies
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

if st.button("Show Recommendations"):
    if selected_movie:
        movie_names = recommend(selected_movie)
        cols = st.columns(5)
        for col, name in zip(cols, movie_names):
            with col:
                st.text(name)
