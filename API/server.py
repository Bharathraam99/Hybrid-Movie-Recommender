from sqlite3.dbapi2 import register_converter
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from controller import get_final_movie_list
import sqlite3
import json

import sys

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@cross_origin()
@app.route('/', methods=['GET'])
def home():
    return "<h1>Hybrid Movie Recommendation System API v1.0</h1><p>This site is a prototype API for movies Frontend</p>"


@app.route('/list')
def list():
    conn = sqlite3.connect(
        'D:\\Project\\HMRS_3.0\\API\\data\\movies_autcomplete.db')
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    rows = db.execute('select title from movies').fetchall()
    conn.close()

    return json.dumps([dict(ix) for ix in rows])


@app.route('/getrec', methods=['POST'])
def getRec():
    return get_final_movie_list(request.data)


app.run()
