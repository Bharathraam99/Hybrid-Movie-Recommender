from csv import reader
import random


def genre_recommendation(genre):
    full_list = []
    final_output = []
    with open('D:\Project\HMRS_3.0\API\data\movies.csv', 'r', encoding="utf8") as read_obj:
        csv_reader = reader(read_obj)
        for i, j in enumerate(csv_reader):
            for each_genre in genre:
                genre_string = j[2]
                if(each_genre in genre_string):
                    full_list.append(j)

    for i in range(20):
        movie_recommend = random.choice(full_list)
        final_output.append(movie_recommend[1])

    return final_output

# movie_emo=dict()
# user_emo=[0.75,0.25]
# full_list=[]
# genre=['Action','Comedy','Thriller']
# final_output=[]

# print(final_output) #JUST TO PRINT FOR TESTING

# def calculate_cosine(temp_list):
#     for i in range(2):
#         x = user_emo[i]; y = temp_list[i]
#         sumxx += x*x
#         sumyy += y*y
#         sumxy += x*y
#     return sumxy/math.sqrt(sumxx*sumyy)

# USING COSINE SIMILARITY
# for k in full_list:
#     temp_list=[]
#     postive=k[3]
#     negative=[4]
#     temp_list.append(postive)
#     temp_list.append(negative)
#     movie_emo[k[1]]=calculate_cosine(temp_list)
#
#
# sorted_tuples = sorted(movie_emo.items(), key=lambda item: item[1])
# sorted_dict = {k: v for k, v in sorted_tuples}
# list_movie=list(sorted_dict.keys());
# for i in list_movie:
#     final_output.append(i)
