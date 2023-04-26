from dataclasses import dataclass
import flask
import flask_cors
import json
from os import environ
import time
from typing import Any, Callable, Dict, List, Optional

import client
from client import AlbumTrack, AudioFeatures, SpotifyClient, Track
from merge_sort import merge_sort, functional_merge_sort
from shell_sort import shell_sort

@dataclass
class ResponseCache:
    # a map from artist id to tracks received from api
    tracks: Dict[str, List[Track]]

@dataclass
class Results:
    time_to_sort: float
    tracks: List[Track]
    
app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

spotify_client: Optional[SpotifyClient] = None
response_cache: ResponseCache = ResponseCache({})

def main() -> None:
    client_id = environ.get('CLIENT_ID')
    client_secret = environ.get('CLIENT_SECRET')
    port = environ.get('PORT')
    
    assert not client_id is None
    assert not client_secret is None
    assert not port is None

    global spotify_client
    spotify_client = SpotifyClient(client_id, client_secret)

    print('starting server...')
    app.run(host='0.0.0.0', port=int(port))

@app.route('/all_tracks_by/<name>/<feature>/<algorithm>')
def all_tracks_by(name: str, feature: str, algorithm: str) -> flask.Response:
    print(f'request: all tracks by \'{name}\', sort by \'{feature}\', using \'{algorithm}\'')

    cmp = get_cmp(feature)

    if cmp is None:
        return flask.jsonify({ 'error': 'invalid_feature' })

    if not algorithm in ['shell', 'imperative_merge', 'functional_merge']:
        return flask.jsonify({ 'error': 'invalid_algorithm' })
    
    # spotify client will never be none if it is initialized in main
    assert not spotify_client is None
    
    artist_id: Optional[str] = spotify_client.artist_id(name)

    if artist_id is None:
        return flask.jsonify({ 'error': 'artist_not_found' })

    tracks: List[Track] = []

    if artist_id in response_cache.tracks:
        tracks = response_cache.tracks[artist_id]
    else:
        print(f'artist id was not found in cache. requesting tracks from api.')

        artist_albums = spotify_client.artist_albums(artist_id)

        if not artist_albums is None:
            track_ids: List[AlbumTrack] = []
            for album in artist_albums:
                album_tracks = spotify_client.album_tracks(album)
                if not album_tracks is None:
                    track_ids += album_tracks
                else:
                    print('error: album tracks api returned nothing')
                    return flask.jsonify({
                        'error': 'api_fail',
                        'message': 'album tracks api returned nothing',
                    })
            # handle if api call failed
            audio_features_response = spotify_client.tracks_audio_features(track_ids)
            if audio_features_response is None:
                return flask.jsonify({
                    'error': 'api_fail',
                    'message': 'audio features api returned nothing'
                })
            else:
                tracks = audio_features_response

    # add tracks to cache
    response_cache.tracks.update({artist_id: tracks})

    # sort the tracks list
    sort_start_time = time.time()
    if algorithm == 'shell':
        shell_sort(tracks, cmp)
    elif algorithm == 'imperative_merge':
        merge_sort(tracks, 0, len(tracks) - 1, cmp)
    elif algorithm == 'functional_merge':
        tracks = functional_merge_sort(tracks, cmp)
    sort_end_time = time.time()

    results = Results(sort_end_time - sort_start_time, tracks)
    
    return flask.jsonify(results)
    
@app.route('/ok')
def ok() -> flask.Response:
    return flask.jsonify({})

# Get the comparison function for a certain audio feature.
# If the feature is not valid, this returns `None`.
def get_cmp(feature: str) -> Optional[Callable[[Track, Track], bool]]:
    features = {
        'acousticness': lambda l, r: l.features.acousticness < r.features.acousticness,
        'danceability': lambda l, r: l.features.danceability < r.features.danceability,
        'duration_ms': lambda l, r: l.features.duration_ms < r.features.duration_ms,
        'energy': lambda l, r: l.features.energy < r.features.energy,
        'instrumentalness': lambda l, r: l.features.instrumentalness < r.features.instrumentalness,
        'liveness': lambda l, r: l.features.liveness < r.features.liveness,
        'speechiness': lambda l, r: l.features.speechiness < r.features.speechiness,
        'loudness': lambda l, r: l.features.loudness < r.features.loudness,
        'tempo': lambda l, r: l.features.tempo < r.features.tempo,
        'valence': lambda l, r: l.features.valence < r.features.valence,
    }

    if feature in features:
        return features[feature]
    else:
        return None

if __name__ == '__main__':
    main()
