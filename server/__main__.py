import flask
import flask_caching
import json
from os import environ
import time
from typing import Any, Dict

import client

app = flask.Flask(__name__)
flask_cache = flask_caching.Cache()

def main() -> None:
    client_id = environ.get('CLIENT_ID')
    client_secret = environ.get('CLIENT_SECRET')

    spotify_client = client.get_spotify_client(client_id, client_secret)
    assert not spotify_client is None

    flask_cache.init_app(app, { 'CACHE_TYPE': 'SimpleCache' })
    flask_cache.set('spotify_client', spotify_client)

    app.run()

@app.route('/artist_top_tracks/<name>')
def artist_top_tracks(name: str) -> Dict[str, str]:
    spotify_client: Any = flask_cache.get('spotify_client')

    result = spotify_client.artist_top_tracks(name)

    if result is None:
        return flask.jsonify({ 'result': 'error' })
    else:
        return app.response_class(
            response=result,
            status=200,
            mimetype='application/json'
        )

if __name__ == '__main__':
    main()

@app.route('/all_tracks_by/<name>')
def all_tracks_by(name: str) -> Dict[str, str]:
    return {}