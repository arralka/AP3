from helpers.lyric_reader import LyricReader
from helpers.universal_reader import UniversalLyricReader
from Part3.LyricModel3 import LyricModel3
from Part3.SongGenerator3 import SongGenerator3


artist = 'Linkin Park'
ngram = 2
seed = None
song = 'VCVCVV'
chorus = 'AABBCC'
verse = 'AABB'

if artist is not None:
    print("Producing lyrics for:", artist, '\n\n')
    lyrics = LyricReader(artist)
else:
    print("Producing lyrics for all artists", '\n\n')
    lyrics = UniversalLyricReader()

model = LyricModel3(lyrics, ngram, seed=seed, max_lyrics=20000)
song_gen = SongGenerator3(song, chorus, verse)

song = song_gen.create_song(model)

print(song)



