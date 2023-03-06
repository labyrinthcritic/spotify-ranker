import flask
import flask_caching
import json
import time
from typing import Any, Dict

import client

# uh oh! global variable!
app = flask.Flask(__name__)
flask_cache = flask_caching.Cache()

def main() -> None:
    with open('secrets.json', 'r') as file:
        config = json.load(file)

    spotify_client = client.get_spotify_client(config['client_id'], config['client_secret'])
    assert not spotify_client is None

    flask_cache.init_app(app, { 'CACHE_TYPE': 'SimpleCache' })
    flask_cache.set('spotify_client', spotify_client)

    app.run()

@app.route('/artist_top_tracks/<name>')
def artist_top_tracks(name: str) -> Dict[str, str]:
    spotify_client: Any = flask_cache.get('spotify_client')

    result = spotify_client.artist_top_tracks(name)

    if result is None:
        return { 'result': 'error' }
    else:
        return result

if __name__ == '__main__':
    main()

@app.route('/all_tracks_by/<name>')
def all_tracks_by(name: str) -> Dict[str, str]:
    return {}