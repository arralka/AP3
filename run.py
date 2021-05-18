from helpers.lyric_reader import LyricReader
from helpers.universal_reader import UniversalLyricReader
from Part2.LyricModel2 import LyricModel2
from Part2.SongGenerator2 import SongGenerator2
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-artist', type=str, help='an integer for the accumulator', default='Linkin Park')
parser.add_argument('-ngram', type=int, help='Number of words back for each state (n in ngrams)', default=3)
parser.add_argument('-lines', type=int, help='Number of lines to produce', default=8)
parser.add_argument('-seed', type=int, help='Random seed for reproducibility', default=None)
parser.add_argument('-part', type=int, help='Random seed for reproducibility', default=None)
parser.add_argument('-song', type=str, help='String structure of song - made of V=Verse and Chorus=C - i.e. VCVCV',
                    default='VCVCVV')
parser.add_argument('-chorus', type=str, help='Chorus rhyming structure, each letter is a line, '
                                              'matching letters rhyme (except X)', default='AABBCC')
parser.add_argument('-verse', type=str, help='Verse rhyming structure, each letter is a line, '
                                              'matching letters rhyme (except X)', default='AABB')

args = parser.parse_args()

artist = args.artist

if artist is not None:
    print("Producing lyrics for:", artist, '\n\n')
    lyrics = LyricReader(artist)
else:
    print("Producing lyrics for all artists", '\n\n')
    lyrics = UniversalLyricReader()

model = LyricModel2(lyrics, args.ngram, seed=args.seed)
song_gen = SongGenerator2(args.song, args.chorus, args.verse)
song = song_gen.create_song(model)

print(song)
