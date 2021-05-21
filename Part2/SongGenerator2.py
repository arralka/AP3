from tqdm import tqdm

from Part1.LyricModel import LyricModel


class SongGenerator2:
    def __init__(self, song_structure, chorus_rhyme, verse_rhyme):
        """
        Creates a song from markov lyric model

        :param chorus_length: Number of lines per chorus
        :param verse_length: Number of lines per verse
        :param song_structure: String of C's and V's referring to structure of song where C is chorus and V is verse
        :param chorus_rhyme: String of letters referring to rhyming structure of chorus i.e. ABAB or AABB,
            where like letters will rhyme, except X

        :param chorus_rhyme: String of letters referring to rhyming structure of verse i.e. ABAB or AABB,
            where like letters will rhyme, except X
        """
        self.song_structure = [ch.upper() for ch in song_structure if ch.upper() in ['C', 'V']]
        self.chorus_rhyme = chorus_rhyme
        self.verse_rhyme = verse_rhyme

    def create_song(self, model):
        chorus = self._create_chorus(model)

        lyrics = "\n"
        verse_count = 1
        for section in tqdm(self.song_structure, desc="Generating Lyrics"):
            if section == 'C':
                lyrics += "[CHORUS]\n"
                lyrics += chorus
            else:
                lyrics += f'[VERSE {verse_count}]\n'
                lyrics += self._create_verse(model)
                verse_count += 1
            lyrics += '\n\n'

        return lyrics

    def _create_chorus(self, model):
        return '\n'.join(model.create_lyrics(self.chorus_rhyme))

    def _create_verse(self, model):
        return '\n'.join(model.create_lyrics(self.verse_rhyme))

