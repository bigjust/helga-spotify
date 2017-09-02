import unittest

from helga_spotify import process_spotify_url


class PluginTest(unittest.TestCase):

    def test_spotify_artist(self):
        response = process_spotify_url('artist', '5MbNzCW3qokGyoo9giHA3V')

        self.assertIn(
            'EARTHGANG',
            response
        )

    def test_spotify_song(self):
        response = process_spotify_url('track', '6fUHMhwKBSmetq2T1PvCKK')

        self.assertEqual(
            response,
            'EARTHGANG - Liquor Sto\''
        )

    def test_spotify_album(self):
        response = process_spotify_url('album', '3bYMVNcOHLDv2z6yWEl3yb')

        self.assertEqual(
            response,
            'EARTHGANG - Strays with Rabies',
        )
