from helpers.lyric_reader import LyricReader
from helpers.universal_reader import UniversalLyricReader
from Part2.LyricModel2 import LyricModel2
from Part2.SongGenerator2 import SongGenerator2

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

model = LyricModel2(lyrics, ngram, seed=seed, max_lyrics=20000)
song_gen = SongGenerator2(song, chorus, verse)

song = song_gen.create_song(model)

print(song)



