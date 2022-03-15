from classifier import KNearestNeighbours
import streamlit as st
from streamlit_lottie import st_lottie
import json
from bs4 import BeautifulSoup
import requests, io
import PIL.Image
from urllib.request import urlopen
import os
from googleapiclient.discovery import build
import pandas as pd

st.set_page_config(page_title="Tv Series Recommender", page_icon="📺", layout="wide")

# Define a function that we can use to load lottie files from a link.
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

col1, col2 = st.columns([1, 3])
with col1:
    lottie = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_khzniaya.json")
    st_lottie(lottie, width=300, height=300)

with col2:
    st.write("""
    ## TV Series Recommender
    ##### This app will help you to find the best TV series for you.""")

# Load the tv data and tv titles
df = pd.read_csv("imdb_tv_series.csv")
with open("./Data/tv_data.json", "r+", encoding="utf-8") as f:
    data = json.load(f)
with open("./Data/tv_titles.json", "r+", encoding="utf-8") as f:
    tv_titles = json.load(f)

youtube_api_key = os.environ.get("tv_rec_youtube_api")
youtube = build("youtube", "v3", developerKey=youtube_api_key)

def poster_fetcher(imdb_link):
    # Display the poster
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, "html.parser")
    imdb_dp = s_data.find("meta", property="og:image")
    poster_link = imdb_dp.attrs["content"]
    u = urlopen(poster_link)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((250, 400), PIL.Image.ANTIALIAS)
    st.image(image)

def get_tv_info(imdb_link):
    # Display the information the tv series
    url_data = requests.get(imdb_link).text
    s_data = BeautifulSoup(url_data, "html.parser")
    imdb_content = s_data.find("meta", property="og:description")
    tv_description = imdb_content.attrs["content"]
    tv_description = str(tv_description).split(".")
    tv_director = tv_description[0]
    tv_title = s_data.find("meta", property="og:title")
    tv_title = tv_title.attrs["content"]
    tv_year = tv_title.split("(")[1].split(")")[0]
    tv_cast = str(tv_description[1]).replace("With", "Cast: ").strip()
    tv_story = "Plot Summary: " + s_data.find("span", {"data-testid": "plot-xl"}).text + "."
    #get rating from span class="sc-7ab21ed2-1 jGRxWM"
    # rating = s_data.find("span", {"class": "sc-7ab21ed2-1 jGRxWM"}).text
    # get  total votes from div class = "sc-7ab21ed2-3 dPVcnq"
    rating = s_data.find("div", {"class": "sc-7ab21ed2-3 dPVcnq"}).text 
    


    # get genres from df if imdb_link are matching
    if imdb_link in df["IMDB_Link"].values:
        tv_genres = df.loc[df["IMDB_Link"] == imdb_link, "Genres"].values[0]
    else:
       tv_genres = "Not Found"
    
    # get runtime from df if imdb_link are matching
    if imdb_link in df["IMDB_Link"].values:
        tv_runtime = df.loc[df["IMDB_Link"] == imdb_link, "Runtime_minutes"].values[0]
    else:
        tv_runtime = "Not Found"
    
    request = youtube.search().list(part="snippet", channelType="any", maxResults=1, q=f"{tv_title} Official Trailer")
    response = request.execute()
    trailer_link = [f"https://www.youtube.com/watch?v={video['id']['videoId']}" \
    for video in response['items']]

    tv_rating = "Total Rating count: " + rating
    return tv_director, tv_cast, tv_story, tv_rating, tv_year, trailer_link, tv_genres, tv_runtime

def knn_tv_recommender(test_point, k):
    # Create dummy target variable for the KNN classifier
    target = [0 for item in tv_titles]
    # Instantiate the KNN classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Print the list of top k recommended tv series
    table = []
    for i in model.indices:
        # Append the tv series title and its imdb link
        table.append([tv_titles[i][0], tv_titles[i][2],data[i][-1]])
    print(table)
    return table

def run_recommender():
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    tv_series = [tv_title[0] for tv_title in tv_titles]
    category = ["Select a recommendation category", "Tv Series based", "Genre based"]
    category_option = st.selectbox("Select a recommendation type", category)
    if category_option == category[0]:
        st.error("Please select a recommendation type")

    elif category_option == category[1]:
        select_tv = st.selectbox("Please select a Tv Series:", tv_series)
        number_of_rec = st.slider("How many recommendations do you want?", min_value=5, max_value=20, step=1, value=5)
        genres = data[tv_series.index(select_tv)]
        test_points = genres
        table = knn_tv_recommender(test_points, number_of_rec+1)
        table.pop(0)
        c = 0
        if st.button("Show recommendations"):
            for tv_serie, link, ratings in table:
                c+=1
                director, cast, story, total_rating, tv_year, trailer_link, tv_genres, tv_runtime = get_tv_info(link)
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f"(**{c}**) [**{tv_serie}**]({link}) **({tv_year})**")
                    poster_fetcher(link)
                    st.markdown(f"**{director}**")
                    st.markdown(f"**{cast}**")
                    st.markdown(f"**{story}**")
                    st.markdown(f"**Runtime: {tv_runtime:.0f} minutes.**")
                    st.markdown(f"**Genres: {tv_genres} .**")
                    st.markdown(f"**{total_rating}**")
                    st.markdown(f"**IMDB Rating: {str(ratings)} ⭐**")
                with col4:
                    st.video(trailer_link[0])

    elif category_option == category[2]:
        select_genre = st.multiselect("Please select a genre:", genres)
        if select_genre:
            imdb_score = st.slider("Choose an IMDB score:", min_value=1, max_value=10, step=1, value=7)
            number_of_rec = st.slider("How many recommendations do you want?", min_value=5, max_value=20, step=1, value=5)
            test_point = [1 if genre in select_genre else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn_tv_recommender(test_point, number_of_rec)
            c = 0
            if st.button("Show recommendations"):
                for tv_serie, link, ratings in table:
                    c+=1
                    director, cast, story, total_rating, tv_year, trailer_link, tv_genres, tv_runtime = get_tv_info(link)
                    col5, col6 = st.columns(2)
                    with col5:
                        st.markdown(f"(**{c}**) [**{tv_serie}**]({link}) **({tv_year})**")
                        poster_fetcher(link)
                        st.markdown(f"**{director}**")
                        st.markdown(f"**{cast}**")
                        st.markdown(f"**{story}**")
                        st.markdown(f"**Runtime: {tv_runtime:.0f} minutes.**")
                        st.markdown(f"**Genres: {tv_genres} .**")
                        st.markdown(f"**{total_rating}**")
                        st.markdown(f"**IMDB Rating: {str(ratings)} ⭐**")
                    with col6:
                        st.video(trailer_link[0])

run_recommender()