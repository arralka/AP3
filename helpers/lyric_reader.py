import os
import re
import string


class LyricReader:
    """
    Reads Lyrics from Open Lyrics Database and cleans into a format for use with Markov Chain model
    """
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.artist_files = self._get_artist_files()
        self.raw_lyrics = self._get_lyrics()
        self.lyrics = self._parse_lyrics()

    def _get_artist_files(self):
        """
        Gets list of artist files
        :return: list of artist files
        """
        resource_path = f'resources/{self.artist_name[0].upper()}/{self.artist_name}'
        albums = os.listdir(resource_path)
        songs = []
        for album in albums:
            if album != '.DS_Store':
                songs += [f'{resource_path}/{album}/{song}' for song in os.listdir(f'{resource_path}/{album}')]
        return songs

    def _get_lyrics(self):
        """
        Creates dictionary matching songs to thier raw lyrics
        :return:
        """
        lyrics = {}
        for song in self.artist_files:
            with open(song, 'r',encoding="utf-8") as f:
                lyrics[song] = f.readlines()[0:-8]
        return lyrics

    def _parse_lyrics(self):
        """
        Transforms raw lyrics into a long list of cleaned and formatted lyrics for use with MarkovMusic class
        :return:
        """
        print("Parsing Lyrics...")
        cc = []
        for key in self.raw_lyrics.keys():
            for line in self.raw_lyrics[key]:
                parsed = re.sub(r'[^\x00-\x7F]+', '', line)
                parsed = parsed.translate(str.maketrans('', '', string.punctuation)).lower().replace('’', '').replace(
                    '“', '')
                cc += [parsed]

        concat = ['<s> ' + ' '.join(reversed(c.replace('\n', '').split(' '))) + ' </s>' for c in cc if c != '\n']
        return concat
