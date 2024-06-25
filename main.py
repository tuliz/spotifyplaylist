from bs4 import BeautifulSoup
import requests
from spotify import Spotify

spotify = Spotify()

# Getting the year of choice to get the top songs of that time
year_choice = input('what year you would like to travel to. type the date in YYY-MM-DD format: ')

# Sending a Get request to to get the HTML code of the website
URL =f'https://www.billboard.com/charts/hot-100/{year_choice}'
response = requests.get(URL)
response.raise_for_status()
data = response.text

# Start of Web Scraping with Beautiful Soup
soup = BeautifulSoup(data, 'html.parser')

# Getting the Info And Tags that includes the Song name and the Singer Name
songs_html = soup.find_all(name='h3', id="title-of-a-story", class_="a-no-trucate")
singers_html = soup.find_all(name='span', class_='a-no-trucate')

# Getting the Texts of the Song and Singer, on the way fixing the text by splitting it
songs_list_fix = [song.getText().split('\t')[9] for song in songs_html]
singers_list_fix = [singer.getText().split('\t')[2].split('\n')[0] for singer in singers_html]

# Build a list with Dicts each has keys of Singer and Song
song_list = [{'singer': singers_list_fix[n], 'song_name': songs_list_fix[n]} for n in range(len(songs_list_fix) - 1)]

# After getting the songs names and artist from billabord in a list create new spotify playlist
spotify.create_playlist(year_choice)

# Send the songs list from billabord and search spotify after the songs IDS
spotify.find_songs_url(song_list)
