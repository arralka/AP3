import re

import pandas as pd
from nltk import ngrams
import numpy as np
from helpers.lyric_reader import LyricReader


class LyricModel:
    """
    Discrete Time Markov Chain model class to produce lyrics from corpus
    """
    def __init__(self, lyric_reader: LyricReader, n, seed=None):
        """
        :param lyric_reader: LyricReader object loaded with lyric data from Open Lyric Database
        :param n: number of words back for each state (the n in ngrams)
        """
        self.n_count = n
        self.lyric_reader = lyric_reader
        self.lyrics = lyric_reader.lyrics
        self.P = self._build_P()

        if seed is not None:
            np.random.seed(seed)

    def _build_P(self):
        """
        Build P matrix for

        :return: Stochastic matrix P
        """
        print("Creating P...")
        ngram_list = []
        state_list = []
        word_list = []

        # Collect occurences of each ngram
        for l in self.lyrics:
            l = re.sub(' +', ' ', f"{'<s> ' * (self.n_count - 2)}{l}").strip()
            ngram_list += [' '.join(list(ng)) for ng in ngrams(l.split(' '), self.n_count)]
            state_list += [' '.join(list(ng)) for ng in ngrams(l.split(' '), self.n_count - 1)]
            word_list += l.split(' ')

        ngram_count = {ng: ngram_list.count(ng) for ng in set(ngram_list)}
        state_count = {s: state_list.count(s) for s in set(state_list)}
        word_count = {w: word_list.count(w) for w in set(word_list)}

        self.unique_words = set(word_list)

        prob_dict = {}
        states = sorted(state_count.keys())
        words = sorted(word_count.keys())

        # Find transfer probability
        for state in states:
            count = state_count[state]
            prob_dict[state] = {}
            for word in words:
                prob_dict[state][word] = ngram_count.get(f'{state} {word}', 0) / count

        # Transform </s> into absorbing state
        for key in prob_dict.keys():
            if key.split(' ')[-1] == '</s>':
                prob_dict[key]['</s>'] = 1

        # Turn into P matrix
        P = pd.DataFrame(prob_dict).transpose()
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
