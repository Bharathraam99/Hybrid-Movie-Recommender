from tweet_fetcher import fetch_tweet
from CBF import get_movie_recommendation
from TBF import fetch_genre
from cosine_calc import get_suggestions
from module3 import genre_recommendation
import random
import json


def cbf_compute(movies_list):
    cbf_movies = []
    for movie in movies_list:
        res_list = get_movie_recommendation(movie)
        cbf_movies.extend(res_list)
    return cbf_movies


def get_final_movie_list(data):
    response_data = dict()

    twitter_id = json.loads(data)['twitterId']
    selected_movies = json.loads(data)["selectedMovies"]

    cbf_movies = []
    cosine_suggestions = []
    genre_list = []
    genre = []
    final_movie_list = []

    try:
        # CBF result list
        cbf_movies = cbf_compute(selected_movies)
        print("CBF output => " + str(len(cbf_movies)), flush=True)

        if twitter_id != "":
            # returns emotion and cleaned tweet as dict
            twitter_data = fetch_tweet(twitter_id)
            twitter_cleaned_string = twitter_data["cleaned_tweet"]
            twitter_user_emotion = twitter_data["emotion_range"]

            # predict genre using module 2 ML
            genre = list(fetch_genre(twitter_cleaned_string)[0])

            # movies from cosine recommendations
            cosine_suggestions = get_suggestions(twitter_user_emotion)
            print("Cosine output => " + str(len(cosine_suggestions)), flush=True)

            # genre recommendation
            genre_list = genre_recommendation(genre)
            print("genre_list output => " + str(len(genre_list)), flush=True)

        combined_movie_list = cbf_movies + cosine_suggestions + genre_list

        print("combined_movie_list output => " +
              str(len(combined_movie_list)), flush=True)

        for i in range(20):
            movie_recommend = random.choice(combined_movie_list)
            final_movie_list.append(movie_recommend)

        print("final_movie_list output => " +
              str(len(final_movie_list)), flush=True)

        for i in final_movie_list:
            print(i, flush=True)

    except Exception as e:
        print(e, flush=True)

    response_data["moviesList"] = list(set(final_movie_list))
    response_data["predictedGenre"] = genre

    return json.dumps(response_data)


# twitter_id = "VP"
# selected_movies = ["Jumanji", "Grumpier Old Men", "Sabrina", "Balto", "Casino"]

# # CBF result list
# cbf_movies = cbf_compute(selected_movies)

# # returns emotion and cleaned tweet as dict
# twitter_data = fetch_tweet(twitter_id)
# twitter_cleaned_string = twitter_data["cleaned_tweet"]
# twitter_user_emotion = twitter_data["emotion_range"]

# genre = fetch_genre(twitter_cleaned_string)
# cosine_suggestions = get_suggestions(twitter_user_emotion)

# print("-------------------- CBF -------------------")
# print(cbf_movies)

# print(" ----------------  twitter data ------------------")
# print(twitter_data)

# print("----------------------------- genre ----------------------")
# print(genre)

# print("---------------------- cosine suggestions ---------------")
# print(cosine_suggestions)
