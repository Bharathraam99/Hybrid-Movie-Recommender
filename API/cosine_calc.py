import csv
from math import *
import sqlite3
from sqlite3 import Error


recommended_movies = list()


def fetch_movie_name(id, conn):
    cur = conn.cursor()
    cur.execute(" SELECT title from movie_name where id= ?", id)

    rows = cur.fetchall()

    for row in rows:
        recommended_movies.append(row[0])


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])), 3)


def cosine_similarity(x, y):
    numerator = sum(a*b for a, b in zip(x, y))
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator), 3)


# ----------------------------------------------------------
def get_suggestions(user_emo):
    conn = create_connection(r"D:\\Project\\HMRS_3.0\\API\\data\\movies.db")
    dict1 = {}

    with open('D:\\Project\\HMRS_3.0\\API\\data\\pd_emotions.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            x = list([float(row[1]), float(row[2])])
            try:
                dict1[row[0]] = cosine_similarity(user_emo, x)
            except:
                dict1[row[0]] = 0

    final_dict = dict(
        sorted(dict1.items(), key=lambda item: item[1])[::-1][:20])

    for i in list(final_dict.keys()):
        fetch_movie_name([i], conn)

    return recommended_movies
