import base64
from dataclasses import dataclass
from functools import cache
import json
import requests
import time
from typing import Dict, List, Optional

API_URL = 'https://api.spotify.com/v1'

@dataclass
class AudioFeatures:
    acousticness: float
    danceability: float
    duration_ms: float
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    speechiness: float
    tempo: float
    valence: float

@dataclass
class Track:
    id: str
    name: str
    features: AudioFeatures

# Part of the response from `SpotifyClient::get_album_tracks`.
@dataclass
class AlbumTrack:
    id: str
    name: str

class SpotifyClient:
    client_id: str
    client_secret: str
    access_token: Optional[str] = None

    last_authorized_time: float
    token_expiration: int

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

        self.reauthorize()

    def reauthorize(self):
        response = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Authorization': b'Basic ' + base64.b64encode((self.client_id + ':' + self.client_secret).encode('ascii'))
            },
            data={
                'grant_type': 'client_credentials'
            }
        )
        if response.ok:
            self.last_authorized_time = time.time()
            
            obj = response.json()
            self.access_token = obj['access_token']
            self.token_expiration = obj['expires_in']
        else:
            raise 'reauthorizaton failed'

    def check_reauthorization(self):
        if time.time() - self.last_authorized_time > self.token_expiration:
            reauthorize()

    # Get an artist's ID by searching their name.
    @cache
    def artist_id(self, name: str) -> Optional[str]:
        self.check_reauthorization()
        
        response = requests.get(
            f'{API_URL}/search',
            headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
            params={
                'type': 'artist',
                'q': name
            },
        )

        if response.ok:
            return response.json()['artists']['items'][0]['id']
        else:
            return None

    # Get the IDs of all albums by an artist from their artist ID.
    @cache
    def artist_albums(self, artist_id: str) -> Optional[List[str]]:
        self.check_reauthorization()
        
        response = requests.get(
            f'{API_URL}/artists/{artist_id}/albums',
            headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
            params={
                'market': 'US',
                'limit': '50',
            },
        )

        if response.ok:
            res_obj = response.json()
            return [album['id'] for album in res_obj['items']]
        else:
            return None

    # Get the IDs of all tracks on an album from its album ID.
    @cache
    def album_tracks(self, album_id: str) -> Optional[List[AlbumTrack]]:
        self.check_reauthorization()
        
        response = requests.get(
            f'{API_URL}/albums/{album_id}/tracks',
            headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
            params={
                'market': 'US',
                'limit': '50',
            },
        )

        if response.ok:
            res_obj = response.json()
            return [AlbumTrack(track['id'], track['name']) for track in res_obj['items']]
        else:
            return None

    def tracks_audio_features(self, input_tracks: List[AlbumTrack]) -> Optional[List[Track]]:
        self.check_reauthorization()
        
        total_tracks = []

        for group in chunks(input_tracks, 100):
            group_str = ','.join([track.id for track in group])
            response = requests.get(
                f'{API_URL}/audio-features',
                headers={ 'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json' },
                params={
                    'ids': group_str,
                },
            )

            if response.ok:
                res_obj = response.json()
                features = res_obj['audio_features']
                
                total_tracks += [Track(track.id, track.name, AudioFeatures(
                    features['acousticness'],
                    features['danceability'],
                    features['duration_ms'],
                    features['energy'],
                    features['instrumentalness'],
                    features['liveness'],
                    features['loudness'],
                    features['speechiness'],
                    features['tempo'],
                    features['valence'],
                )) for (track, features) in zip(group, features)]
            else:
                print(f'tracks_audio_features request failed: {response.status_code}')

        return total_tracks

def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]