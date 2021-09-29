# Imports initialiseren voor het project.
import pandas as pd
import plotly.express as px
import spotipy
from IPython.core.display import display
from spotipy.oauth2 import SpotifyClientCredentials

# Maak een Spotify object instantie van de SpotiPy package.
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Lees the id's van de top 20 meest gevolgde artiesten van Spotify in een csv bestand.
artist_ids = pd.read_csv('top20followedartists.csv').columns
print(artist_ids.values)

# Haal alle artiesten data op van de Spotify Rest API d.m.v. de artiesten id's
# en formatteer de json data naar de gewenste vorm.
sp_artists = sp.artists(artist_ids)['artists']
df_artists = pd.json_normalize(sp_artists).set_index('name').sort_values('followers.total')
display(df_artists.head())

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
fig.show()

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
fig.show()

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
fig.show()
