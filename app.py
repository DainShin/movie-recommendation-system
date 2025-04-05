import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

# Create Movie and TmDb object to use tmdb 
movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'fdfd2228235a69f1627fcb50dca81c80'  #tmdb site. username: DainShin pw: 0000
# tmdb.language ='ko-KR'

# Make function
def get_recommendations(title):
    # Get the index through the title
    idx = movies[movies['title'] == title].index[0] 

    # In the cosine similarity matrix, get (idx, similarity) 
    sim_scores = list(enumerate(cosine_sim[idx]))

    # descending
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)

    # indexing (excluding itself, get 10 results)
    sim_scores = sim_scores[1:11]

    # extracting 10 indices of the recommendations
    movie_indices = [i[0] for i in sim_scores]

    # through index, get the title
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i] 
        details = movie.details(id)

        # Check if the image exists
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + details['poster_path']
        else:
            image_path = 'no_image.jpg'


        images.append(image_path) 
        titles.append(details['title']) 

    return images, titles  # get_recommendations end  


# Get data
movies = pickle.load(open('movies.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle','rb'))

# Make UI
st.set_page_config(layout='wide') # To see the whole screen
st.header('Inflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)

# When the button is clicked
#  streamlit run app.py
if st.button('Recommend'):
    with st.spinner('Please wait...'): # progress bar
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0,2): # 0,1
            cols = st.columns(5) # making columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1  
