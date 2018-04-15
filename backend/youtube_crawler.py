'''IMPORTANT if you are running this on windows
Download the ffmpeg package from http://ffmpeg.zeranoe.com/builds/, unzip it,
copy ALL the contents of the Bin directory to the directory where youtube-dl.exe
is located. If you are on linux installing ffmpeg with apt-get should work'''

from __future__ import unicode_literals
import youtube_dl
#import urllib.parse
import urllib2
import json
from apiclient.discovery import build
import random, string
import webbrowser
import isodate
import datetime as dt
import pprint

with open('config.json') as json_data_file:
    key = json.load(json_data_file)
DEVELOPER_KEY = key['MY_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MUSIC = "10"

#creates random string
def randomword(length):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))


#searches the youtube api using a random string and music category
def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
              developerKey = DEVELOPER_KEY)

    #this searches for 5 youtube vids with a random string of the music
    #category and places the result in search_response we're only using
    # a three letter string this length could be experimented with to find what
    #will give you better or more "random" results
    search_response = youtube.search().list(
        q=randomword(3),
        part="id, snippet",
        type="video",
        videoCategoryId=MUSIC,
        maxResults= 5,
        videoEmbeddable = 'true',
        order = 'date'
        ).execute()

    videos = []
    channelIds = []
    userVids = []
    userUploads = []

    for search_result in search_response.get("items",[]):
        #pprint.pprint(search_result)
        if search_result["id"]["kind"] == "youtube#video":

            channelId = search_result["snippet"]["channelId"]
            #print("\n\nchannelId: " + channelId + "\n\n")

            channelIDDetails = youtube.channels().list(
                part = "contentDetails",
                id = channelId
            ).execute().get("items")

            uploads = channelIDDetails[0]["contentDetails"]["relatedPlaylists"]["uploads"]

            uploadData = youtube.playlistItems().list(
                part = "id, snippet",
                maxResults = 5,
                playlistId = uploads
            ).execute().get("items",[])

            tempUserVids = []
            userVids = []
            for item in uploadData:
                if item["kind"] == "youtube#playlistItem" and item["snippet"]["position"] > 0:
                    tempUserVids.append(item["snippet"]["resourceId"]["videoId"])
            userVids.append(random.sample(tempUserVids, len(tempUserVids)))

            #flatten the user vids list
            flatUserVids = []
            for sublist in userVids:
                for item in sublist:
                    flatUserVids.append(item)

            #getting the video information
            videoStat = []
            for vid in flatUserVids:
                videoStat.append(youtube.videos().list(
                    part = 'status, snippet, contentDetails',
                    id = vid
                ).execute().get("items"))

            for stat in videoStat:
                length = isodate.parse_duration(stat[0]["contentDetails"]["duration"])
                #print(length)
                privacy = stat[0]["status"]["privacyStatus"]
                category = stat[0]["snippet"]["categoryId"]
                maxMins = dt.timedelta(minutes=8)
                minMins = dt.timedelta(minutes=1)
                if privacy == "public" and category == MUSIC and length > minMins and length < maxMins:
                    if stat[0] == None:
                        break
                    else:
                        return stat[0]["id"]


            continue



#function that grabs a random youtubevideo id is using randomyoutube api
#This is the api that the above algorithm is based upon
def getRandomId():
    url = 'https://randomyoutube.net/api/getvid?api_token=TktN4bc321ZUZvidMKRVyKHcacVXnwlHCUkm8qb3c22YelU2hiR7FIQgBM6t'
    response = urllib2.urlopen(url)
    jsonResponse = response.read()
    stringResponse = json.loads(jsonResponse)
    return stringResponse['vid']


#uses youtube_dl to download only the audio portions of youtube link
def download_song(url):
    #outtmpl option determines where your file will be output
    ydl_opts = {
        'ignoreerrors': True,
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'wav',
            'preferredquality' : '192',
        }],
        'outtmpl' : './music/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except TypeError as e:
            print(e)


#just a main script to test everything is working
if __name__ == "__main__":
    youtubeURL = 'https://www.youtube.com/watch'
    vidID = youtube_search()
    url = '?v='.join([youtubeURL, vidID])
    #print(url)
    #webbrowser.open(url)
    download_song(url)
