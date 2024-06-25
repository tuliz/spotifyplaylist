import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Spotify:
    def __init__(self):

        # Get Enviroment Varaibles
        load_dotenv()
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        self.SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')

        # Authenticate to Spotify with spotipy package
        self.scope = "playlist-modify-private"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, scope=self.scope))
        self.user_id = self.sp.current_user()['id']
        self.playlist_id = None
        self.song_id_list = []

    # Create new playlist in Spotify
    def create_playlist(self,year_choice):
        self.playlist_id = self.sp.user_playlist_create(user=self.user_id,name=f'TopBillabord{year_choice}',public=False)

    # Pass list of songs and singers and find the songs URLS in Spotify
    def find_songs_url(self, songs):

        song_url_list = []
        print('Fetching Song IDS....')

        for song in songs:

            song_no_space = song['singer'].replace(' ', '%%2520')
            singer_no_space = song['song_name'].replace(' ', '%%2520')
            id = self.sp.search(q=f'remaster%2025track:{song_no_space}%2025artist:{singer_no_space}',limit=10,type='track')

            for song_id in id['tracks']['items']:
                if song_id['name'] == song['song_name'] and song_id['external_urls']['spotify']:
                    song_url_list.append(song_id['external_urls']['spotify'])
                    break

        print('Fetched Songs IDS from Spotify...')
        self.add_to_playlist(song_url_list)

    # Get the List of Songs URLS Found in Spotify and Add the Songs to the Playlist
    def add_to_playlist(self, songs_url):
        print('Adding songs to playlist...')
        response = self.sp.playlist_add_items(self.playlist_id['id'], songs_url)
        print(response)
