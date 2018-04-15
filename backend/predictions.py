import os, shutil
import youtube_crawler as yc
import quick_test as qt
from time import gmtime, strftime
from flask_pymongo import PyMongo
from pymongo import MongoClient



def jazz(post):
    jazz_songs = db.jazz
    post_id = jazz_songs.insert_one(post).inserted_id
def rock(post):
    rock_songs = db.rock
    post_id = rock_songs.insert_one(post).inserted_id
def blues(post):
    blues_songs = db.blues
    post_id = blues_songs.insert_one(post).inserted_id
def pop(post):
    pop_songs = db.pop
    post_id = pop_songs.insert_one(post).inserted_id
def reggae(post):
    reggae_songs = db.reggae
    post_id = reggae_songs.insert_one(post).inserted_id
def hiphop(post):
    hiphop_songs = db.hiphop
    post_id = hiphop_songs.insert_one(post).inserted_id
def disco(post):
    disco_songs = db.disco
    post_id = disco_songs.insert_one(post).inserted_id
def country(post):
    country_songs = db.country
    post_id = country_songs.insert_one(post).inserted_id
def classical(post):
    classical_songs = db.classical
    post_id = classical_songs.insert_one(post).inserted_id
def metal(post):
    metal_songs = db.metal
    post_id = metal_songs.insert_one(post).inserted_id


def putInDb(arg, post):
    switcher = {
        'jazz': jazz,
        'rock': rock,
        'blues': blues,
        'pop': pop,
        'reggae': reggae,
        'hiphop': hiphop,
        'disco': disco,
        'country': country,
        'classical': classical,
        'metal': metal
    }
    func = switcher.get(arg, lambda:'invalid genre')
    func(post)

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
    try:
        genre, song_name, mean = qt.run()
    except Exception as e:
        print(e)
        continue

    #put song data in database
    client = MongoClient()
    db = client.song_db
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    post = {"name": song_name[:-4],
            "genre": genre,
            "url": url,
            "vidID": vidID,
            "date": time,
            "mean": mean}
    putInDb(genre, post)
    print("url: {} \ngenre: {} \ntime entered: {} \n".format(url, genre, time))
