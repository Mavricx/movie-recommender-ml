import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("TMDB_API_KEY")


movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": api_key
}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return None



def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


st.title("Movie Recommender System")

selected_movie_name=st.selectbox(
    'How would you like to be contacted?',
   movies['title'].values  )

if st.button("Recommend"):
    names, recommendations = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]
    for idx, col in enumerate(columns):
        with col:
            st.text(names[idx])
            if recommendations[idx]:
                st.image(recommendations[idx])
            else:
                st.write("Poster not available")





# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import os
# from dotenv import load_dotenv
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load .env file
# load_dotenv()

# api_key = os.getenv("TMDB_API_KEY")

# # File paths
# MOVIES_DICT_PATH = "app/movies_dict.pkl"
# SIMILARITY_PATH = "app/similarity.pkl"  

# # ---------------------------
# # Function to build similarity.pkl
# # ---------------------------
# def build_similarity():
#     print("🔄 Building similarity.pkl from dataset...")

#     # Load movies dictionary or CSV
#     if os.path.exists(MOVIES_DICT_PATH):
#         movies_dict = pickle.load(open(MOVIES_DICT_PATH, 'rb'))
#         movies_df = pd.DataFrame(movies_dict)
#     elif os.path.exists(MOVIES_CSV_PATH):
#         movies_df = pd.read_csv(MOVIES_CSV_PATH)
#     else:
#         st.error("No dataset found to build similarity matrix.")
#         st.stop()

#     # Vectorize the 'tags' column or create your own combined text field
#     if 'tags' in movies_df.columns:
#         text_data = movies_df['tags']
#     else:
#         # fallback: combine title + genres if tags don't exist
#         text_data = movies_df['title'] + " " + movies_df['genres']

#     cv = CountVectorizer(max_features=5000, stop_words='english')
#     vectors = cv.fit_transform(text_data).toarray()
#     sim = cosine_similarity(vectors)

#     # Save similarity matrix
#     with open(SIMILARITY_PATH, 'wb') as f:
#         pickle.dump(sim, f)

#     return movies_df, sim

# # ---------------------------
# # Load or build data
# # ---------------------------
# if os.path.exists(SIMILARITY_PATH) and os.path.exists(MOVIES_DICT_PATH):
#     movies_dict = pickle.load(open(MOVIES_DICT_PATH, 'rb'))
#     movies = pd.DataFrame(movies_dict)
#     similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))
# else:
#     movies, similarity = build_similarity()

# # ---------------------------
# # API fetch function
# # ---------------------------
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#     headers = {
#         "accept": "application/json",
#         "Authorization": api_key
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         data = response.json()
#         if 'poster_path' in data and data['poster_path']:
#             return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
#     return None

# # ---------------------------
# # Recommendation function
# # ---------------------------
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_movies_poster = []

#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_movies_poster.append(fetch_poster(movie_id))

#     return recommended_movies, recommended_movies_poster

# # ---------------------------
# # Streamlit UI
# # ---------------------------
# st.title("Movie Recommender System")

# selected_movie_name = st.selectbox(
#     'Select a movie:',
#     movies['title'].values
# )

# if st.button("Recommend"):
#     names, recommendations = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)

#     for idx, col in enumerate([col1, col2, col3, col4, col5]):
#         with col:
#             st.text(names[idx])
#             if recommendations[idx]:
#                 st.image(recommendations[idx])
#             else:
#                 st.write("Poster not available")
