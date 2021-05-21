from helpers.lyric_reader import LyricReader
from helpers.universal_reader import UniversalLyricReader
from Part1.LyricModel import LyricModel
from Part1.SongGenerator import SongGenerator

artist = 'Linkin Park'
ngram = 2
seed = None
song = 'VCVCVV'
chorus_len = 6
verse_len = 4

if artist is not None:
    print("Producing lyrics for:", artist, '\n\n')
    lyrics = LyricReader(artist)
else:
    print("Producing lyrics for all artists", '\n\n')
    lyrics = UniversalLyricReader()

model = LyricModel(lyrics, ngram, seed=seed, max_lyrics=20000)
song_gen = SongGenerator(song, chorus_len, verse_len)

song = song_gen.create_song(model)

print(song)



