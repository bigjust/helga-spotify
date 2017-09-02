import mock
import responses
import unittest

from helga_spotify import (
    process_spotify_url,
    spotify_api_base,
)

def create_response(spotify_type, spotify_id, json):
    api_url = '{}{}s/{}'.format(
        spotify_api_base,
        spotify_type,
        spotify_id
    )

    responses.add(
        responses.GET,
        api_url,
        json=json,
        status=200
    )


@mock.patch('helga_spotify.get_spotify_token')
class PluginTest(unittest.TestCase):

    def setUp(self):
        create_response(
            'artist',
            '5MbNzCW3qokGyoo9giHA3V',
            {
                'name': 'EARTHGANG',
                'genres': ['hippity-hop', 'escape room'],
            },
        )

        create_response(
            'track',
            '6fUHMhwKBSmetq2T1PvCKK',
            {
                'name': 'Liquor Sto\'',
                'artists': [{'name': 'EARTHGANG'}],
            },
        )

        create_response(
            'album',
            '3bYMVNcOHLDv2z6yWEl3yb',
            {
                'name': 'Strays with Rabies',
                'artists': [{'name': 'EARTHGANG'}],
            },
        )

    @responses.activate
    def test_spotify_artist(self, mock_token):
        mock_token.return_value = '123'
        response = process_spotify_url('artist', '5MbNzCW3qokGyoo9giHA3V')

        self.assertIn(
            response,
            'EARTHGANG (hippity-hop, escape room)'
        )

    @responses.activate
    def test_spotify_song(self, mock_token):
        mock_token.return_value = '123'
        response = process_spotify_url('track', '6fUHMhwKBSmetq2T1PvCKK')

        self.assertEqual(
            response,
            'EARTHGANG - Liquor Sto\''
        )

    @responses.activate
    def test_spotify_album(self, mock_token):
        mock_token.return_value = '123'
        response = process_spotify_url('album', '3bYMVNcOHLDv2z6yWEl3yb')

        self.assertEqual(
            response,
            'EARTHGANG - Strays with Rabies',
        )
