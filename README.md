## TV_Series-Recommender
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)

#### About this project
- Created a dataset of tv shows which has rating greater than 6.0 and has more than 10,000 votes and has been released between 1970-2022 by scraping [the IMDb website](https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&release_date=1970-01-01,2022-02-12&user_rating=6.0,10.0&num_votes=10000,&languages=en&sort=user_rating,desc&count=100&start=) using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library and saving the dataframe to a csv file.
- The dataset contains the following columns:
  - **Title:** The title of the tv series
  - **Year:** The year the tv show was released
  - **Runtime:** The runtime of the tv series
  - **Genre:** The genre of the tv series
  - **Rating:** The rating of the tv series
  - **Votes:** The votes of the tv series
- The recommender system uses the K-Nearest Neighbors algorithm to recommend tv series based on the user's preferences.
- Retrieved the tv series trailers for recommended tv series dynamically, using [Youtube Data API v3](https://developers.google.com/youtube/v3).
- Built the web app using [Streamlit](https://streamlit.io) and deployed it on [Heroku](https://www.heroku.com
).
- You can take a look at the [interactive demo](https://tv-series-rec.herokuapp.com) to see how the recommender system works.
