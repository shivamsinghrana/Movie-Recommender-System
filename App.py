import streamlit as st
import pickle
import pandas as pd
import requests#to hit api we use this poster
def fetch_poster(movie_id):
   response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
   data=response.json()

   return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    #this is empty for append below
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # here we need to fetch movie poster by api
        recommended_movies_posters.append(fetch_poster(movie_id))#here we return movie id get info
    return recommended_movies, recommended_movies_posters
    #here this function is nothing just to return 5 movies name
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender system')
selected_movie_name = st.selectbox(
    'how would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, (name, poster) in enumerate(zip(names, posters)):
        print(name,poster)
        with cols[i % 5]:
            st.text(name)#here we change header to text bcoz text give short form
            st.image(poster)
   # for i in  recommendations:
    #    st.write(i)

