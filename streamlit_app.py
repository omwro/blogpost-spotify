# Imports initialiseren voor het project.
import pandas as pd
import plotly.express as px
import spotipy
from IPython.core.display import display
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import plotly.graph_objects as go
import json

# Streamlit title
st.title("Spotify blog")
st.caption("Klas 3 - Groep 15 - Leden: Nassim, Omer, Max, Emmelotte")

# Maak een Spotify object instantie van de SpotiPy package.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id='5f222d8ae8c744f6815d314bba7709ab',
    client_secret='2e90b0c27de84414ac5a7847d8bc73c9'
))
# Lees the id's van de top 20 meest gevolgde artiesten van Spotify in een csv bestand.
artist_ids = pd.read_csv('top20followedartists.csv').columns
print(artist_ids.values)

# Haal alle artiesten data op van de Spotify Rest API d.m.v. de artiesten id's
# en formatteer de json data naar de gewenste vorm.
sp_artists = sp.artists(artist_ids)['artists']
df_artists = pd.json_normalize(sp_artists).set_index('name').sort_values('followers.total')
display(df_artists.head())

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
st.markdown("## Top 20 meest gevolgde artiesten")
# Een bar plot waarbij het totaal aantal volgers wordt weergeven van de artiesten.
fig = px.bar(df_artists,
             x='followers.total',
             y=df_artists.index,
             color='followers.total',
             labels={'followers.total': 'Totaal aantal volgers'})
fig.update_layout(title="Totaal aantal volgers van de top 20 meest gevolgde artiesten",
                  yaxis_title='Artiest namen',
                  xaxis_title="Totaal aantal volgers in Miljoenen<br>Bron:<a href='https://en.wikipedia.org/wiki/List_of_most-streamed_artists_on_Spotify'>Wikipedia</a>")
fig.update_xaxes(range=[30_000_000, 90_000_000])
st.plotly_chart(fig)

# Een lijn plot waarbij de populariteit wordt weergeven van de artiesten.
# Het verticale rechte lijn is het gemiddelde van de weergegeven artiesten.
fig = px.line(df_artists,
              x='popularity',
              y=df_artists.index,
              text='popularity', height=500)
fig.add_vline(df_artists['popularity'].mean(),
              annotation_text="Gemiddelde",
              annotation_position="bottom right")
fig.update_layout(title="Populariteit van de top 20 meest gevolgde artiesten",
                  yaxis_title='Artiest namen',
                  xaxis_title="Populariteit van artiesten in Spotify")
fig.update_traces(textposition="bottom right")
st.plotly_chart(fig)

# Een pie plot waarbij het hoofd genre wordt weergeven dan de artiesten.
df_artists['main_genre'] = None
df_artists['main_genre'] = df_artists.apply(lambda artist: "hip hop" if "hip hop" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "hip hop" if "reggaeton" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "pop" if "pop" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "pop" if "k-pop" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "pop" if "desi pop" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "rap" if "rap" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)
df_artists['main_genre'] = df_artists.apply(lambda artist: "rock" if "rock" in artist['genres'] and artist['main_genre'] is None else artist['main_genre'], axis=1)

df_artist_main_genre = df_artists['main_genre'].value_counts()
fig = px.pie(df_artist_main_genre,
             values='main_genre',
             names=df_artist_main_genre.index)
fig.update_layout(title="De hoofd genres van de top 20 meest gevolgde artiesten")
fig.update_traces(textposition='inside',
                  textinfo='value+percent')
st.plotly_chart(fig)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
st.markdown("## Eigenschappen van de topnummers")

playlistURL = 'https://open.spotify.com/playlist/596TVWnQdvHEeYyKUXkpDL?si=d36cdf733a8945c5'

#get playlist items
playlist = sp.playlist_items(playlistURL)

# write playlist data to JSON file
with open('data.json', 'w') as f:
    json.dump(playlist, f)

# read the JSON file using pandas to convert to DataFrame
data = json.load(open('data.json'))

df = pd.DataFrame(data)
df.head()

# initialise item ID list
IDlist = []

# get total songs in playlist
totalSongs = df.iloc[0]['total']

# for loop to retreive all song IDs from the playlist
for x in range(0, totalSongs):
    pl_item = df.iloc[x]['items']

    # write playlist data to JSON file
    with open('data.json', 'w') as f:
        json.dump(pl_item, f)

    # read the JSON file using pandas to convert to DataFrame
    data3 = json.load(open('data.json'))
    # find track ID
    itemDF = pd.DataFrame(data3)
    trackID = itemDF['track'].loc['uri']
    IDlist.append(trackID)

# get number of IDs in IDlist
print(len(IDlist))

# create list of track features of all songs
trackFeaturesList = sp.audio_features(tracks=IDlist)
print(trackFeaturesList)

# create empty list to put input song dicts
allSongs = []

# year of first song
year = 1946

# for loop to add track info to the DataFrame
for x in range(0, totalSongs):
    # get song name
    songInfo = sp.track(IDlist[x])
    songName = songInfo['name']

    # get song features
    trackFeatures = trackFeaturesList[x]
    danceability = trackFeatures['danceability']
    energy = trackFeatures['energy']
    loudness = trackFeatures['loudness']
    acousticness = trackFeatures['acousticness']
    tempo = trackFeatures['tempo']

    # create dictionary from song info
    song = {
        'year': year,
        'name': songName,
        'danceability': danceability,
        'energy': energy,
        'loudness': loudness,
        'acousticness': acousticness,
        'tempo': tempo
    }

    # increment year with 1
    year = year + 1

    # add dictionary to list
    allSongs.append(song)

# change list into Pandas DataFrame
allSongsDF = pd.DataFrame(allSongs)
allSongsDF.head()

fig = go.Figure()

features = ['danceability', 'energy', 'loudness', 'acousticness', 'tempo']

for features in features:
    tempDF = allSongsDF[features]
    fig.add_trace(go.Scatter(x=allSongsDF['year'], y=tempDF, name=features, mode='markers'))

    # Add the legend
    my_legend = {'x': 1, 'y': 0,
                 'bgcolor': 'rgb(237, 219, 180)', 'borderwidth': 5}
    # Update the figure
    fig.update_layout({'showlegend': True, 'legend': my_legend},
                      title="Change in audio features throughout the years (1946-2021)")
    fig.update_layout(hovermode="y")

sliders = [
    {'steps': [
        {'method': 'update', 'label': 'Danceability', 'args': [{'visible': [True, False, False, False, False]}]},
        {'method': 'update', 'label': 'Energy', 'args': [{'visible': [False, True, False, False, False]}]},
        {'method': 'update', 'label': 'Loudness', 'args': [{'visible': [False, False, True, False, False]}]},
        {'method': 'update', 'label': 'Acousticness', 'args': [{'visible': [False, False, False, True, False]}]},
        {'method': 'update', 'label': 'Tempo', 'args': [{'visible': [False, False, False, False, True]}]}]}]

fig.update_layout({'sliders': sliders})

st.plotly_chart(fig)
