import base64
import json
import requests
from typing import Dict, List, Optional

API_URL = 'https://api.spotify.com/v1'

class APICache:
    artist_id: Dict[str, str] = {}
    artist_top_tracks: Dict[str, List[Dict[str, str]]] = {}
    artist_albums: Dict[str, str] = {}

class SpotifyClient:
    access_token: str = ''
    cache: APICache = APICache()

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    def artist_id(self, name: str) -> Optional[str]:
        # check cache
        if name in self.cache.artist_id:
            print(f'Found \'{name}\' in cache.')
            return self.cache.artist_id[name]
        
        response = requests.get(
            f'{API_URL}/search',
            headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
            params={
                'type': 'artist',
                'q': name
            }
        )

        if response.ok:
            id = response.json()['artists']['items'][0]['id']
            # add to cache
            self.cache.artist_id[name] = id
            return id
        else:
            return None

    def artist_top_tracks(self, name: str) -> Optional[str]:
        # check cache
        if name in self.cache.artist_top_tracks:
            print(f'Found top tracks of {name} in cache.')
            return json.dumps(self.cache.artist_top_tracks[name])
        
        artist_id = self.artist_id(name)
        if artist_id is None:
            return None

        response = requests.get(
            f'{API_URL}/artists/{artist_id}/top-tracks',
            headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
            params={ 'market': 'US' }
        )

        if response.ok:
            track_list = response.json()['tracks']
            # comprehension to retain only id and name fields
            track_list = [ { i: obj[i] for i in ('id', 'name') } for obj in track_list ]
            self.cache.artist_top_tracks[name] = track_list
            return json.dumps(track_list)
        else:
            return None

def get_spotify_client(client_id: str, client_secret: str) -> Optional[SpotifyClient]:
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={
            'Authorization': b'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('ascii'))
        },
        data={
            'grant_type': 'client_credentials'
        }
    )
    if response.ok:
        return SpotifyClient(response.json()['access_token'])
    else:
        return None
