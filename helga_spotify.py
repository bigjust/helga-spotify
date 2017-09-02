import base64
import re
import requests

from helga import log, settings
from helga.plugins import match

spotify_pattern = re.compile(r'https://open.spotify.com/(?P<type>.*)/(?P<id>.*)')
spotify_api_base = 'https://api.spotify.com/v1/'
spotify_client_id = getattr(settings, 'SPOTIFY_CLIENT_ID')
spotify_secret = getattr(settings, 'SPOTIFY_SECRET')

logger = log.getLogger(__name__)

def get_spotify_token():

    resp = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'client_credentials',
        },
        headers={
            'Authorization': 'Basic {}'.format(
                base64.b64encode('{}:{}'.format(
                    spotify_client_id,
                    spotify_secret,
                ))
            ),
        },
    )

    return resp.json()['access_token']

def process_spotify_url(spotify_type, spotify_id):

    token = get_spotify_token()

    resp = requests.get(
        '{}{}s/{}'.format(
            spotify_api_base,
            spotify_type,
            spotify_id
        ),
        headers={'Authorization': 'Bearer {}'.format(token)}
    )

    resp_json = resp.json()

    if spotify_type == 'artist':
        return '{} ({})'.format(
            resp_json['name'],
            ', '.join(resp_json['genres'])
        )

    return '{} - {}'.format(
        resp_json['artists'][0]['name'],
        resp_json['name']
    )

@match('https://open.spotify.com/(artist|album|track)/(\w+)')
def spotify(client, channel, nick, message, matches):
    match = matches[0]
    return process_spotify_url(match[0], match[1])
