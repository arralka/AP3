from Part1.LyricModel import LyricModel
from Part2.LyricModel2 import LyricModel2
import numpy as np
import pandas as pd
from helpers.lyric_reader import LyricReader
from statistics import mean
import json
import urllib.request as urllib2
import math


class LyricModel3(LyricModel2):
    def __init__(self, lyric_reader: LyricReader, n, seed=None):
        super().__init__(lyric_reader, n, seed)
        print("Ave")
        print(self.artist_average_syllables())
        print("Ave done")

    def syllable_count(self, word):
        word = word.lower()
        with open("resources/syllable_dictionary.json") as file:
            dump = json.load(file)
            if (word in dump) and (dump[word] != None):
                return dump[word]   
            if (word in dump) and (dump[word] == None):
                return 2  # Datamuse lacks the word so we'll just set it to 2 syllables?       
        url='https://api.datamuse.com/words?md=s&max=1&sp=' + word
        data = json.load(urllib2.urlopen(url))
        if len(data) == 0:
            return 2 # Datamuse lacks the word so we'll just set it to 2 syllables?
        return data[0]['numSyllables']

    def artist_average_syllables(self):
        syllables = []
        cache = {}
        for l in self.lyrics:
            wl = l.split()
            # Don't want <s> or </s> and they're at the back/front
            wl.pop()
            wl.pop(0)
            lineSyllableCount = 0
            for w in wl:
                if w in cache:
                    c = cache[w]
                else:
                    c = self.syllable_count(w)
                    cache[w] = c
                lineSyllableCount += c
            syllables.append(lineSyllableCount)
        return math.floor(mean(syllables))
