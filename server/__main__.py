from dataclasses import dataclass
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

@dataclass
class ResponseCache:
    # a map from artist id to tracks received from api
    tracks: Dict[str, List[Track]]

def main() -> None:
    client_id = environ.get('CLIENT_ID')
    client_secret = environ.get('CLIENT_SECRET')
    port = environ.get('PORT')
    
    assert not client_id is None
    assert not client_secret is None
    assert not port is None

    spotify_client = client.get_spotify_client(client_id, client_secret)
    assert not spotify_client is None

    flask_cache.init_app(app, { 'CACHE_TYPE': 'SimpleCache' })
    flask_cache.set('spotify_client', spotify_client)
    flask_cache.set('response_cache', ResponseCache({}))

    print('starting waitress wsgi server...')
    waitress.serve(app, host='0.0.0.0', port=port)

@app.route('/all_tracks_by/<name>/<feature>/<algorithm>')
def all_tracks_by(name: str, feature: str, algorithm: str) -> flask.Response:
    print(f'request: all tracks by \'{name}\', sort by \'{feature}\', using \'{algorithm}\'')

    cmp = get_cmp(feature)

    if cmp is None:
        return flask.jsonify({ 'error': 'invalid_feature' })

    if not algorithm in ['shell', 'imperative_merge', 'functional_merge']:
        return flask.jsonify({ 'error': 'invalid_algorithm' })
    
    cl: Any = flask_cache.get('spotify_client')
    response_cache: Any = flask_cache.get('response_cache')

    assert type(cl) is client.SpotifyClient
    assert type(response_cache) is ResponseCache

    artist_id: Optional[str] = cl.artist_id(name)

    if artist_id is None:
        return flask.jsonify({ 'error': 'artist_not_found' })

    tracks: List[Track] = []

    if artist_id in response_cache.tracks:
        tracks = response_cache.tracks[artist_id]
    else:
        print(f'artist id was not found in cache. requesting tracks from api.')

        artist_albums = cl.artist_albums(artist_id)

        if not artist_albums is None:
            track_ids: List[str] = []
            for album in artist_albums:
                album_tracks = cl.album_tracks(album)
                if not album_tracks is None:
                    track_ids += album_tracks
                else:
                    print('error: album tracks api returned nothing')
                    return flask.jsonify({
                        'error': 'api_fail',
                        'message': 'album tracks api returned nothing',
                    })
            # handle if api call failed
            audio_features_response = cl.tracks_audio_features(track_ids)
            if audio_features_response is None:
                return flask.jsonify({
                    'error': 'api_fail',
                    'message': 'audio features api returned nothing'
                })
            else:
                tracks = audio_features_response

    assert not tracks is None

    # add tracks to cache
    response_cache.tracks.update({artist_id: tracks})
    flask_cache.set('response_cache', response_cache)

    # sort the tracks list
    if algorithm == 'shell':
        shell_sort(tracks, cmp)
    elif algorithm == 'imperative_merge':
        merge_sort(tracks, 0, len(tracks) - 1, cmp)
    elif algorithm == 'functional_merge':
        tracks = functional_merge_sort(tracks, cmp)
    
    return flask.jsonify(tracks)
    
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
