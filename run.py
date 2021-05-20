from Part3.LyricModel3 import LyricModel3
from helpers.lyric_reader import LyricReader
from helpers.universal_reader import UniversalLyricReader
from Part3.SongGenerator3 import SongGenerator3
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
parser.add_argument('-syllables', type=int, help='Number of syllables per line, 0 will use average of artist', default=10) #TODO change default to 0 when submitting

args = parser.parse_args()

artist = args.artist

if artist is not None:
    print("Producing lyrics for:", artist, '\n\n')
    lyrics = LyricReader(artist)
else:
    print("Producing lyrics for all artists", '\n\n')
    lyrics = UniversalLyricReader()

model = LyricModel3(lyrics, args.ngram, args.syllables, seed=args.seed)
song_gen = SongGenerator3(args.song, args.chorus, args.verse)
song = song_gen.create_song(model)

print(song)
