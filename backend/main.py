import os, shutil
import YoutubeCrawler as yc
import quick_test as qt
from time import gmtime, strftime
from flask_pymongo import PyMongo
from pymongo import MongoClient
import time as t
from flask import Flask, jsonify, url_for, redirect, request


# app = Flask(__name__)
# app.config['MONGO_DBNAME'] = 'song_db'
# mongo = PyMongo(app, config_prefix='MONGO')
#
# @app.route('/api', methods=['GET'])
# def get_all_songs():
#     songs = mongo.db.posts
#     output = []
#     for q in songs.find().limit(10):
#         output.append({"name": q['name'], "genre": q['genre'], "url": q['url']})
#     return jsonify(output)
#
# @app.route('/api/<genre>', methods=['GET'])
# def get_song_list(genre):
#     songs = mongo.db.posts
#     output = []
#     for q in songs.find({"genre": genre}).limit(10):
#         output.append({"name": q['name'], "genre": q['genre'], "url": q['url']})
#     return jsonify(output)




#def classify_songs():
while(True):
    #remove songs from the music directory
    path = './music'
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    #download our random youtube song
    youtubeURL = 'https://www.youtube.com/watch'
    vidID = yc.youtube_search()


    try:
        url = '?v='.join([youtubeURL, vidID])
    except TypeError as e:
        print(e)
        continue
    try:
        yc.download_song(url)
    except TypeError as e:
        print(e)
        continue


    #analyze our songs genre
    genre, song_name = qt.run()

    #put song data in database


    client = MongoClient()
    db = client.song_db
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    post = {"name": song_name,
            "genre": genre,
            "url": url,
            "vidID": vidID,
            "date": time}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    #print(post_id)
    print("url: {} \ngenre: {} \ntime entered: {} \n".format(url, genre, time))


# if __name__ == '__main__':
#     app.run(debug=True, port=8085)
