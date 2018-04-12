from flask import Flask, jsonify, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson.objectid import ObjectId
import requests
from flask_cors import CORS

class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))

app = CustomFlask(__name__,
                  static_folder = "../dist/static",
                  template_folder = "/dist")
cors = CORS(app, resources={r"/song/*": {"origins":"*"}})
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})
app.config['MONGO_DBNAME'] = 'song_db'
mongo = PyMongo(app, config_prefix='MONGO')
#APP_URL = "http://127.0.0.1:5000"

# class HelloWorld(Resource):
#     def get(self):
#         song = mongo.db.posts.find({'genre': 'rock'})
#         return{'result': song}

# class Song(Resource):
#     def get(self, genre=None):
#         data = []
#         # song = mongo.db.posts.find_one({"genre":"rock"},{"_id":0})
#         # return jsonify({"data":song})
#         # if genre:
#         #     cursor =  mongo.db.posts.find({"genre": genre}, {"_id":0}).limit(10)
#         #     for song in cursor:
#         #         song['url'] = APP_URL + url_for('songs') + "/" + song.get('id')
#         #         data.append(song)
#         #
#         #     return jsonify({"response": data})
#
#
# #         cursor =  mongo.db.posts.find({}, {"_id":0}).limit(10)
# #         for song in cursor:
# #             print song.get('_id')
# #             #song['url'] = APP_URL + url_for("songs") + "/" + song.get('id')
# #             #data.append(song)
# #
# #         return jsonify({"response": data})
# #
# # api = Api(app)
# # api.add_resource(Song,'/api', endpoint="songs")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

@app.route('/api/song', methods=['GET'])
def get_all_songs():
    songs = mongo.db.posts
    output = []
    for q in songs.find():
        output.append({"name": q['name'], "genre": q['genre'], "url": q['url']})
    return jsonify(output)

@app.route('/api/song/<genre>/', methods=['GET'])
def get_song_list(genre):
    songs = mongo.db.posts
    output = []
    for q in songs.find({"genre": genre}).limit(10):
        output.append({"name": q['name'], "genre": q['genre'], "url": q['url'], "vidID":q['vidID']})
    return jsonify(output)

@app.route('/api/song/one/<genre>', methods=['GET'])
def get_one_song(genre):
    songs = mongo.db.posts.find_one({"genre": genre})
    return jsonify({"name": songs['name'], "genre": songs['genre'], "url": songs['url']})

@app.route('/api/video/<genre>/', methods=['GET'])
def get_one_video(genre):
    songs = mongo.db.posts.find_one({"genre": genre})
    return songs['vidID']


if __name__ == '__main__':
    app.run(debug=True)
