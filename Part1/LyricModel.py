import re

import pandas as pd
from nltk import ngrams
import numpy as np
from helpers.lyric_reader import LyricReader
from collections import Counter
import random
from tqdm import tqdm


class LyricModel:
    """
    Discrete Time Markov Chain model class to produce lyrics from corpus
    """
    def __init__(self, lyric_reader: LyricReader, n, seed=None, max_lyrics=10000):
        """
        :param lyric_reader: LyricReader object loaded with lyric data from Open Lyric Database
        :param n: number of words back for each state (the n in ngrams)
        """
        self.n_count = n
        self.lyric_reader = lyric_reader
        if len(lyric_reader.lyrics) > max_lyrics:
            self.lyrics = random.sample(lyric_reader.lyrics, max_lyrics)
        else:
            self.lyrics = lyric_reader.lyrics
        self.P = self._build_P()
        self.true_P = None

        if seed is not None:
            np.random.seed(seed)

    def _build_P(self):
        """
        Build transition matrix for

        :return: Stochastic matrix P
        """
        print("Creating P...")
        ngram_list = []
        state_list = []
        word_list = []

        # Collect occurences of each ngram
        for l in tqdm(self.lyrics, desc="Collecting n-grams"):
            l = re.sub(' +', ' ', f"{'<s> ' * (self.n_count - 2)}{l}").strip()
            ngram_list += [' '.join(list(ng)) for ng in ngrams(l.split(' '), self.n_count)]
            state_list += [' '.join(list(ng)) for ng in ngrams(l.split(' '), self.n_count - 1)]
            word_list += l.split(' ')

        ngram_count = Counter(ngram_list)
        state_count = Counter(state_list)
        word_count = Counter(word_list)

        self.unique_words = set(word_list)

        states = pd.Series(sorted(state_count.keys()))
        words = pd.Series(sorted(word_count.keys()))
        tqdm.pandas()

        # Find transfer probabilities
        P = pd.DataFrame(states.progress_apply(lambda state: words.apply(lambda word: ngram_count.get(f'{state} {word}', 0) / state_count[state])))
        P.index = states
        P.columns = words

        # Transform </s> into absorbing state
        for key in [k for k in P.columns if k.split(' ')[-1] == '</s>']:
            P.loc[key, '</s>'] = 1

        P.index.name = 'STATE'
        return P

    def create_lyrics(self, line_count: int):
        """
        Generate lyrics

        :param line_count: number of lines to produce
        :return: list of lyric lines
        """

        lines = []
        for i in range(line_count):
            lines.append(self._create_line())
        return lines

    def _create_line(self):
        """
        Creates a single line of lyric
        :return: Randomly generate lyric
        """

        # Initialise starting state
        line = ("<s> "*(self.n_count-1)).strip()
        next_word = self._fetch_word(line)

        # Grab words based on state until hitting absorbing state </s>
        while next_word != "</s>":
            line += ' ' + next_word
            current_state = ' '.join(line.split(' ')[-(self.n_count-1):])
            next_word = self._fetch_word(current_state)

        return ' '.join(reversed(line.replace('<s> ', '').replace(' </s>', '').split(' '))).capitalize()

    def _fetch_word(self, state):
        """
        Randomly generates next word from current state
        :param state: current state in the form of an ngram
        :return: Next word
        """
        r = np.random.rand()
        state_transitions = self.P.loc[state]
        state_transitions = state_transitions[state_transitions>0]

        if len(state_transitions) == 0:
            return '</s>'

        return state_transitions.index[state_transitions.cumsum().searchsorted(r)]

    def create_P(self):
        """
        Create true P matrix (nxn matrix of states)
        """
        if self.true_P is not None:
            return self.true_P

        p_dict = {}
        for state in tqdm(self.P.index, desc='building true P'):
            p_dict[state] = {}
            for word in self.P.columns:
                p_dict[state][' '.join(state.split(' ')[1:] + [word])] = self.P.loc[state, word]

        return pd.DataFrame(p_dict).fillna(0)



