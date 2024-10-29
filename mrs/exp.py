import streamlit as st
import pickle
import pandas as pd
import requests
# demo begins
import tkinter as tk
from PIL import Image, ImageTk  # You may need to install Pillow with pip install pillow
import webbrowser

# YouTube video URL
video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"  # Replace with the desired YouTube URL

# Function to open the YouTube video

# Load your image (movie poster, for example)
poster_image = Image.open("path_to_your_image.jpg")  # Replace with the path to your image
poster_image = poster_image.resize((300, 450))  # Resize as needed
poster_photo = ImageTk.PhotoImage(poster_image)

# Create a label with the poster image
poster_label = tk.Label(root, image=poster_photo)
poster_label.pack()

# Bind the hover (enter and leave) events to open the video
poster_label.bind("<Enter>", open_video)

root.mainloop()
#end of demo
def fetch_poster(movie_id):
    response= requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def fetch_trailer(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}/videos?language=en-US&api_key=d8ed32747c0f30fed3d3599daa49ebc9".format(
            movie_id))
    data = response.json()

    # Assuming the first video result is the trailer
    if 'results' in data and len(data['results']) > 0:
        trailer_key = data['results'][0]['key']
        return "https://www.youtube.com/watch?v=" + trailer_key
    else:
        return "Trailer not available."
def recommend(movie):
    m_index = m[m['title'] == movie].index[0]
    distances = similarity[m_index]
    m_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    recommended_trailer=[]
    for i in m_list:
        movie_id=m.iloc[i[0]].movie_id
        recommended_movies.append(m.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_trailer.append(fetch_trailer(movie_id))
    return recommended_movies,recommended_movies_poster,recommended_trailer
m_dict=pickle.load(open('movies_dict.pkl','rb'))
m=pd.DataFrame(m_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendation System')
selected_movie_name=st.selectbox('Which movie you recently watched?',m['title'].values)
if st.button('Recommend'):
    names,posters,trailer=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])