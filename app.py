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
    idx = movies[movies['title'] == title].index[0]  # movies['title'] 과 전달받은 title이 똑같은것. 인덱스 값은 배열로 넘어오기때문에 index[0]

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
        id = movies['id'].iloc[i] # pickle을 통해서 데이터를 가져온 movies에는 영화 id, title 값있음
        details = movie.details(id)

        # Check if the image exists
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + details['poster_path']
        else:
            image_path = 'no_image.jpg'


        images.append(image_path) 
        titles.append(details['title']) # tmdb 에서 한국어 버전으로 변경 가능

    return images, titles  # get_recommendations end  


# 데이터 불러오기
movies = pickle.load(open('movies.pickle','rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle','rb'))

# 화면 만들기
st.set_page_config(layout='wide') # 전체화면 보기 위해
st.header('Inflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)

# 버튼이 클릭됐을때 
#  streamlit run app.py
if st.button('Recommend'):
    with st.spinner('Please wait...'): # progress bar
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0,2): # 0~2 미만까지 
            cols = st.columns(5) # columns(5) : 5개 컬럼 만들기
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1  # 5개 컬럼에 이미지와 제목을 넣었으면 다음 행으로 넘어가서 다시 이미지, 타이틀 넣음