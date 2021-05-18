"""
    Generates a universal lyrics file
"""

import os
from helpers.lyric_reader import LyricReader


class UniversalLyricReader(LyricReader):
    """
    Reads Lyrics from all files in Open Lyrics Database and cleans into a format for use with Markov Chain model
    """

    def __init__(self):
        super().__init__(None)

    def _get_artist_files(self):
        """
        Gets list of artist files
        :return: list of artist files
        """
        resource_path = f'resources'
        songs = []
        for letter in os.listdir(resource_path):
            for artist in os.listdir(f'{resource_path}/{letter}'):
                for album in os.listdir(f'{resource_path}/{letter}/{artist}'):
                    songs += [f'{resource_path}/{letter}/{artist}/{album}/{song}' for song in
                              os.listdir(f'{resource_path}/{letter}/{artist}/{album}')]

        return songs
