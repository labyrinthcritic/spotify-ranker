import flask
import flask_caching
import json
from os import environ
import time
from typing import Any, Callable, Dict, List, Optional
import waitress

import client
from client import AudioFeatures, Track
from merge_sort import merge_sort, functional_merge_sort
from shell_sort import shell_sort

app = flask.Flask(__name__)
flask_cache = flask_caching.Cache()

def main() -> None:
    client_id = environ.get('CLIENT_ID')
    client_secret = environ.get('CLIENT_SECRET')

    assert not client_id is None
    assert not client_secret is None

    spotify_client = client.get_spotify_client(client_id, client_secret)
    assert not spotify_client is None

    flask_cache.init_app(app, { 'CACHE_TYPE': 'SimpleCache' })
    flask_cache.set('spotify_client', spotify_client)

    print('starting waitress wsgi server...')
    waitress.serve(app, host='0.0.0.0', port=8080)

@app.route('/all_tracks_by/<name>/<feature>/<algorithm>')
def all_tracks_by(name: str, feature: str, algorithm: str) -> flask.Response:
    print(f'request: all tracks by \'{name}\'')

    cmp = get_cmp(feature)

    if cmp is None:
        return flask.jsonify({ 'error': 'invalid_feature' })

    if not algorithm in ['shell', 'imperative_merge', 'functional_merge']:
        return flask.jsonify({ 'error': 'invalid_algorithm' })
    
    cl: Any = flask_cache.get('spotify_client')

    assert type(cl) is client.SpotifyClient

    artist_id = cl.artist_id(name);
    if not artist_id is None:
        artist_albums = cl.artist_albums(artist_id)

        if not artist_albums is None:
            tracks: List[str] = []
            for album in artist_albums:
                album_tracks = cl.album_tracks(album)
                if not album_tracks is None:
                    tracks += cl.album_tracks(album)
                else:
                    print('error: album tracks api returned nothing')
                    return flask.jsonify({
                        'error': 'api_fail',
                        message: 'album tracks api returned nothing',
                    })
            audio_features = cl.tracks_audio_features(tracks)

            # sort the audio features list

            if algorithm == 'shell':
                shell_sort(audio_features, cmp)
            elif algorithm == 'imperative_merge':
                merge_sort(audio_features, 0, len(audio_features) - 1, cmp)
            elif algorithm == 'functional_merge':
                audio_features = functional_merge_sort(audio_features, cmp)
            
            return flask.jsonify(audio_features)
    
    return flask.jsonify({})

@app.route('/ok')
def ok() -> flask.Response:
    return flask.jsonify({})

# Get the comparison function for a certain audio feature.
# If the feature is not valid, this returns `None`.
def get_cmp(feature: str) -> Optional[Callable[[Track, Track], bool]]:
    features = {
        'acousticness': lambda l, r: l.features.acousticness < r.features.acousticness,
        'danceability': lambda l, r: l.features.danceability < r.features.danceability,
        'duration': lambda l, r: l.features.duration_ms < r.features.duration_ms,
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
