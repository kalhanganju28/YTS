import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl
import re
from secrets import spotify_token, spotify_user_id


class CreatePlaylist:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}
        #Give your playlist ID here
        self.playlist_id = "playlist_ID"

        #Give name to your ney spotify playlist
        self.playlist_name = "Playlist Name"

        #Give description to your playlist
        self.playlist_description = "Playlist Description"

    def get_youtube_client(self):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_playlist_videos(self):

        request = self.youtube_client.playlistItems().list(
            part = 'contentDetails',
            playlistId = self.playlist_id,
            maxResults = 100,
            pageToken = None
        )

        playlist_response = request.execute()

        vid_ids = []

        for item in playlist_response['items'] :
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request =  self.youtube_client.videos().list(
            part = "snippet,contentDetails,statistics",
            id = ','.join(vid_ids)
        )

        vid_response = vid_request.execute()

        # collect each video and get important information
        for item in vid_response["items"]:
            video_title = item["snippet"]["title"]

            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)

            song_name = video["title"]

            if "artist" in video.keys() : 
                artist = video["artist"]   
            else :
                artist = None

            print('old : ', song_name)
            print('old : ', artist)
            
            if(artist is not None) : 
                song_name = song_name.replace(artist, '').replace('-', '').replace('ft.', '').replace(',', '').lstrip(' ').rstrip(' ')
                song_name = re.sub("[\(\[].*?[\)\]]", "", song_name)
                artist = artist.split(",")[0]
            
            print('new : ', song_name)
            print('new : ', artist)

            if song_name is not None and artist is not None:

                spotify_uri_temp = self.get_spotify_uri(song_name, artist)
                print('spotify URI : ')
                print(spotify_uri_temp)

                if spotify_uri_temp is not None :

                    self.all_song_info[video_title] = {
                        "youtube_url": youtube_url,
                        "song_name": song_name,
                        "artist": artist,
                        "spotify_uri": spotify_uri_temp

                    }

    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": self.playlist_name,
            "description": self.playlist_description,
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
        )

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()

        if "tracks" not in response_json.keys() :
            return None

        print(response_json.keys())

        songs = response_json["tracks"]["items"]

        print(len(songs))

        if len(songs) == 0 :
            return None
        else :
            uri = songs[0]["uri"]
            return uri

    def add_song_to_playlist(self):
        self.get_playlist_videos()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        print("URI's \n")
        print(uris)

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
