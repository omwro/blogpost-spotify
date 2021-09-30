# Imports initialiseren voor het project.
import pandas as pd
import numpy as np
import plotly.express as px
import spotipy
from IPython.core.display import display
from matplotlib import pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import plotly.graph_objects as go
import json
from itertools import cycle

# Streamlit title
st.title("Spotify blog")
st.caption("Klas 3 - Groep 15 - Leden: Nassim, Omer, Max, Emmelotte")

st.markdown("#### API & CSV")
st.markdown("We maken gebruik van de "
            "[Spotify API](https://developer.spotify.com/documentation/web-api/reference/) "
            "om alle data op te halen. Als package gebruiken we "
            "[SpotiPy](https://spotipy.readthedocs.io/en/2.19.0/?highlight=artist#welcome-to-spotipy) "
            "om gemakkelijk via python de requesten te sturen naar de spotify server. Vervolgens gebruiken we "
            "[Wikipedia](https://en.wikipedia.org/wiki/List_of_most-streamed_artists_on_Spotify) "
            "om de top 20 artiesten te vinden en daarvan een speciaal gemaakt csv file te maken. Daarnaast gebruiken "
            "we ook een dataset van "
            "[kaggle](https://www.kaggle.com/iamsumat/spotify-top-2000s-mega-dataset) "
            "voor de top 2000 nummer van altijd en [Kaggle](https://www.kaggle.com/leonardopena/top50spotify2019) "
            "voor het ophalen van de top 50 buitenlandse nummers.")

st.markdown("#### Kwaliteit")
st.markdown("We maken gebruik van de officiële spotify api en weten dat dit aan hoge kwaliteitstandaarden houdt. "
            "Ook gebruiken we CSV datasets die vooraf zijn gecontroleerd op de datakwaliteit en of de data binnen de "
            "dataset relevant is voor onze geval, zoals de nummer eigenschappen. Ons enige probleem is dat streamlit "
            "paar momenten kan nemen om alle api requesten te sturen en ontvangen.")


st.markdown("#### Toon/verberg secties")
check1 = st.checkbox('Top 20 artiesten', True)
check2 = st.checkbox('Nummer eigenschappen', True)
check3 = st.checkbox('Top 2.000 nummers', True)
check4 = st.checkbox('Top 50 nummers buitenland', True)
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

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
if check1:
    st.markdown("## Top 20 meest gevolgde artiesten")
    st.markdown("##### In de onderstaande bar chart zijn de top 20 artiesten te zien met de meeste volgers op Spotify.")
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
if check1:
    st.plotly_chart(fig)
    st.markdown("```\nfig = px.bar(df_artists, x='followers.total', y=df_artists.index, color='followers.total',labels={'followers.total': 'Totaal aantal volgers'})"
                "\nfig.update_layout(title='Totaal aantal volgers van de top 20 meest gevolgde artiesten', yaxis_title='Artiest namen', xaxis_title='Totaal aantal volgers in Miljoenen<br>Bron:<a href='https://en.wikipedia.org/wiki/List_of_most-streamed_artists_on_Spotify'>Wikipedia</a>')"
                "\nfig.update_xaxes(range=[30_000_000, 90_000_000])```")
    st.markdown("##### In de onderstaande grafiek is de populariteit op Spotify van de top 20 meest gevolgde artiesten te zien.")
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
if check1:
    st.plotly_chart(fig)
    # st.markdown("``````")

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
st.markdown("##### In de onderstaande pie chart is de verdeling van (hoofd)genres binnen de top 20 meest gevolgde artiesten te zien.")
fig = px.pie(df_artist_main_genre,
             values='main_genre',
             names=df_artist_main_genre.index)
fig.update_layout(title="De hoofd genres van de top 20 meest gevolgde artiesten")
fig.update_traces(textposition='inside',
                  textinfo='value+percent')
if check1:
    st.plotly_chart(fig)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if check2:
    st.markdown("## Eigenschappen van de topnummers")
    st.markdown("##### In de onderstaande grafiek zijn de ontwikkelingen in audio eigenschappen door de jaren heen te zien. De nummers in deze grafiek zijn de #1 Year-End Songs van Billboard tussen 1946 en 2021.")

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
                 'bgcolor': 'rgb(255, 79, 79)', 'borderwidth': 5}
    # Update the figure
    fig.update_layout({'showlegend': True, 'legend': my_legend},
                      title="Veranderingen in audio eigenschappen van #1 hits door de jaren heen (1946-2021)")
    fig.update_layout(hovermode="y")

sliders = [
    {'steps': [
        {'method': 'update', 'label': 'Danceability', 'args': [{'visible': [True, False, False, False, False]}]},
        {'method': 'update', 'label': 'Energy', 'args': [{'visible': [False, True, False, False, False]}]},
        {'method': 'update', 'label': 'Loudness', 'args': [{'visible': [False, False, True, False, False]}]},
        {'method': 'update', 'label': 'Acousticness', 'args': [{'visible': [False, False, False, True, False]}]},
        {'method': 'update', 'label': 'Tempo', 'args': [{'visible': [False, False, False, False, True]}]}]}]

fig.update_layout({'sliders': sliders})

if check2:
    st.plotly_chart(fig)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if check3:
    st.markdown("## Top 2000")
    

df_spotify = pd.read_csv('Spotify-2000.csv')
print(df_spotify)

print(df_spotify['Top Genre'].describe())

print(df_spotify['Top Genre'].unique())
df_spotify['Genre category'] = None

# ROCK
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "rock" if "rock" in song['Top Genre'] else song['Top Genre'], axis=1)

# POP
df_spotify['Genre category'] = df_spotify.apply(lambda song: "pop" if "pop" in song['Top Genre'] else song['Top Genre'],
                                                axis=1)

# HIP-HOP
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "hip-hop" if "hip hop" in song['Top Genre'] else song['Top Genre'], axis=1)

print(df_spotify)

print(df_spotify['Genre category'])

df_spotify['Genre category'] = None

# ROCK
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "rock" if "rock" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "rock" if "indie" in song['Top Genre'] else song['Genre category'], axis=1)

# POP
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "pop" if "pop" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "pop" if "adult standards" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "pop" if "permanent wave" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "pop" if "boy band" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "pop" if "neo mellow" in song['Top Genre'] else song['Genre category'], axis=1)

# HIP-HOP
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "hip-hop" if "hip hop" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "hip-hop" if "g funk" in song['Top Genre'] else song['Genre category'], axis=1)

# JAZZ
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "jazz" if "jazz" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "jazz" if "bebop" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "jazz" if "dutch cabaret" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "jazz" if "soul" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "jazz" if "disco" in song['Top Genre'] else song['Genre category'], axis=1)

# METAL
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "metal" if "metal" in song['Top Genre'] else song['Genre category'], axis=1)

# RAP
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "rap" if "rap" in song['Top Genre'] else song['Genre category'], axis=1)

# CLASSIC
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "classical" if "classic" in song['Top Genre'] else song['Genre category'], axis=1)

# BLUES
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "blues" if "folk" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "blues" if "americana" in song['Top Genre'] else song['Genre category'], axis=1)

# HOUSE
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "house" if "big room" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "house" if "house" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "house" if "trance" in song['Top Genre'] else song['Genre category'], axis=1)
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "house" if "edm" in song['Top Genre'] else song['Genre category'], axis=1)

# OTHER
df_spotify['Genre category'] = df_spotify.apply(
    lambda song: "other" if song['Genre category'] is None else song['Genre category'], axis=1)

print(df_spotify['Genre category'].unique())

fig = go.Figure()

features = ['Popularity', 'Loudness (dB)', 'Danceability', 'Valence', 'Speechiness', 'Energy']

colors = cycle(
    ['rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(255, 127, 14)', 'rgb(150, 190, 170)', 'rgb(255, 64, 64)',
     'rgb(100, 149, 237)'])

for feature in features:
    genres = df_spotify[feature]
    fig.add_trace(go.Box(x=df_spotify['Genre category'], y=genres, name=feature, marker_color=next(colors)))

dropdown_spotify = [
    {'label': 'Popularity', 'method': 'update', 'args': [{'visible': [True, False, False, False, False, False]},
                                                         {'title': 'Popularity'}]},
    {'label': 'Loudness (dB)', 'method': 'update', 'args': [{'visible': [False, True, False, False, False, False]},
                                                            {'title': 'Loudness (dB)'}]},
    {'label': 'Danceability', 'method': 'update', 'args': [{'visible': [False, False, True, False, False, False]},
                                                           {'title': 'Danceability'}]},
    {'label': 'Valence', 'method': 'update', 'args': [{'visible': [False, False, False, True, False, False]},
                                                      {'title': 'Valence'}]},
    {'label': 'Speechiness', 'method': 'update', 'args': [{'visible': [False, False, False, False, True, False]},
                                                          {'title': 'Speechiness'}]},
    {'label': 'Energy', 'method': 'update', 'args': [{'visible': [False, False, False, False, False, True]},
                                                     {'title': 'Energy'}]},
]

fig.update_layout({'updatemenus': [
    {'type': 'dropdown', 'x': 1.2, 'y': 0.2, 'showactive': True, 'active': 0, 'buttons': dropdown_spotify}]})
fig.update_layout(showlegend=True)
fig.update_xaxes(title='genre')

if check3:
    st.markdown("#### Boxplot genres top 2000")
    st.markdown("##### De onderstaande boxplots geven de verschillen in audio eigenschappen tussen verschillende genres weer.")
    st.plotly_chart(fig)

fig = go.Figure()

colors = cycle(
    ['rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(255, 127, 14)', 'rgb(150, 190, 170)', 'rgb(255, 64, 64)',
     'rgb(100, 149, 237)'])

for feature in features:
    genres1 = df_spotify[feature]
    fig.add_trace(go.Bar(x=df_spotify['Genre category'], y=genres1, name=feature, marker_color=next(colors)))

dropdown_spotify = [
    {'label': 'Popularity', 'method': 'update', 'args': [{'visible': [True, False, False, False, False, False]},
                                                         {'title': 'Popularity'}]},
    {'label': 'Loudness (dB)', 'method': 'update', 'args': [{'visible': [False, True, False, False, False, False]},
                                                            {'title': 'Loudness (dB)'}]},
    {'label': 'Danceability', 'method': 'update', 'args': [{'visible': [False, False, True, False, False, False]},
                                                           {'title': 'Danceability'}]},
    {'label': 'Valence', 'method': 'update', 'args': [{'visible': [False, False, False, True, False, False]},
                                                      {'title': 'Valence'}]},
    {'label': 'Speechiness', 'method': 'update', 'args': [{'visible': [False, False, False, False, True, False]},
                                                          {'title': 'Speechiness'}]},
    {'label': 'Energy', 'method': 'update', 'args': [{'visible': [False, False, False, False, False, True]},
                                                     {'title': 'Energy'}]},
]

fig.update_layout({'updatemenus': [
    {'type': 'dropdown', 'x': 1.2, 'y': 0.2, 'showactive': True, 'active': 0, 'buttons': dropdown_spotify}]})
fig.update_layout(showlegend=True)
fig.update_xaxes(title='genre')
fig.update_yaxes(title='sum')
fig.update_traces(marker_line_width=0)

if check3:
    st.markdown("#### Barchart genres top 2000")
    st.markdown("##### De onderstaande bar chart geeft de verschillen in audio eigenschappen tussen verschillende genres weer.")
    st.plotly_chart(fig)

sum_loudness = sum(df_spotify['Loudness (dB)'])

print(sum_loudness)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
if check4:
    st.markdown("## Top 50 nummers buitenland")

# Volledig overzicht global top 50 chart
data = pd.read_csv('top50.csv')
df = pd.DataFrame(data)
df.describe()

# Weergaven van hoeveelheid tracks in de top 50 chart per artiest
Artist = pd.DataFrame(df['Artist.Name'].value_counts()).reset_index()
Artist.columns = ['Artiesten', 'Tracks']
graph = px.bar(Artist, x='Artiesten', y='Tracks', color='Artiesten',
               title='Weergaven van hoeveelheid tracks in de top 50 chart per artiest')
if check4:
    st.plotly_chart(graph)

# overzicht creeren van de eerste values in de kolommen, om zo ook een overzicht te krijgen van de kolommen
# die in de csv file zitten
df.head()

data_df = pd.read_csv("SpotifyTopSongsByCountry - May 2020.csv")
pd.read_csv("SpotifyTopSongsByCountry - May 2020.csv")

# Overzicht maken van de top 10 tracks in de global top 50 charts
data_df.head(10)

# Pie Chart verdeling aantal tracks per continent in de top 50 global
fig = px.pie(data_df, values='Rank', names='Continent', hole=0.6)
fig.update_layout(annotations=[
    dict(text='"Pie Chart verdeling aantal tracks per continent in de top 50 global"', font_size=16, y=1.1,
         showarrow=False)])
if check4:
    st.plotly_chart(fig)

# # Aantal 'unieke' landen in de top 50 global
# unique_countries = data_df["Country"].unique()
# unique_countries = unique_countries[unique_countries != "Global"]
#
# # Aantal 'unieke' continenten in de top 50 global
# data_df["Continent"].unique()
#
# # Bar plot oorsprong tracks per continent in de global top 50 chart
# continent_value_counts = (data_df["Continent"].value_counts() / 50).astype("int32")
# continent_value_counts = continent_value_counts.drop("Global")
# height = continent_value_counts.values
# bars = continent_value_counts.index
# y_pos = range(0, 12, 2)
#
# fig = plt.figure()
# ax = fig.gca()
# ax.grid()
#
# plt.bar(y_pos, height, color=['orange', 'red', 'green', 'blue', 'cyan', 'yellow'], width=1.2)
#
# plt.xticks(y_pos, bars, color="#424242")
# plt.yticks(color="#424242")
# for i, v in enumerate(height):
#     ax.text((i) * 2 - 0.1, v + 0.5, str(v), color='#424242')
# plt.title("Oorsprong liedjes per continent in de Top 50", y=1, fontsize=16)
#
# if check4:
#     st.plotly_chart(plt)
#
# # Bar plot over de top 10 tracks die het vaakst voorkomen in de global top 50 chart
# top10_tracks = data_df["Title"].value_counts()[:10].sort_values(ascending=True)
# height = top10_tracks.values
# bars = top10_tracks.index
# y_pos = np.arange(len(bars))
#
# fig = plt.figure(figsize=[11, 7], frameon=False)
# ax = fig.gca()
#
# plt.barh(y_pos, height,
#          color=['orange', 'red', 'green', 'blue', 'cyan', 'yellow', 'purple', 'magenta', 'brown', 'lightblue'],
#          height=0.8)
#
# plt.xticks()
# plt.yticks(y_pos, bars)
# plt.xlabel("Number of occurances in charts")
#
# for i, v in enumerate(height):
#     ax.text(v + 1, i, str(v))
# plt.title("Top 10 meest voorkomende tracks", fontsize=16)
#
# if check4:
#     st.plotly_chart(plt)
#
# # Alle unieke ALbums in de dataframe op een rij
# data_df["Album"].unique()
