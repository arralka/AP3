from Part1.LyricModel import LyricModel
import numpy as np
import pandas as pd
from helpers.lyric_reader import LyricReader
import requests


class LyricModel2(LyricModel):
    def __init__(self, lyric_reader: LyricReader, n, seed=None, max_lyrics=10000):
        super().__init__(lyric_reader, n, seed, max_lyrics)

    def create_lyrics(self, rhyme_structure):
        """
        Generate lyrics

        :param line_count: number of lines to produce
        :return: list of lyric lines
        """

        lines = []
        rhymes = {}
        for r in rhyme_structure:
            if r in rhymes.keys() and r != 'X':
                line = self._create_line(rhyme_constraint=rhymes[r])
            else:
                line = self._create_line()

            lines.append(line)
            rhymes[r] = line.split(' ')[-1]

        return lines

    def _create_line(self, rhyme_constraint=None):
        """
        Creates a single line of lyric
        :return: Randomly generate lyric
        """

        if rhyme_constraint is None:
            return super()._create_line()

        # Initialise starting state
        line = ("<s> " * (self.n_count - 1)).strip()

        # Get rhyming words
        rhymes = self.get_rhymes(rhyme_constraint)

        if rhymes is None: # If rhyming API query returns nothing get normal word
            next_word = self._fetch_word(line)
        else:
            next_word = self._fetch_rhyming_word(line, rhymes)

        # Grab words based on state until hitting absorbing state </s>
        while next_word != "</s>":
            line += ' ' + next_word
            current_state = ' '.join(line.split(' ')[-(self.n_count - 1):])
            next_word = self._fetch_word(current_state)

        return ' '.join(reversed(line.replace('<s> ', '').replace(' </s>', '').split(' '))).capitalize()

    def get_rhymes(self, word):
        try:
            r = requests.get(f'https://api.datamuse.com/words?rel_rhy={word}')
            rhymes = pd.DataFrame(r.json()).set_index('word')
            rhymes['scores'] = rhymes['score']/rhymes['score'].sum()
            return rhymes
        except Exception as e:
            return None

    def _fetch_rhyming_word(self, state, rhymes):
        r = np.random.rand()

        state_transitions = self.P.loc[state]
        state_transitions = state_transitions[state_transitions > 0]
        state_transitions = state_transitions.filter(rhymes.index)

        if len(state_transitions) == 0:
            return self._fetch_word(state)

        state_transitions = state_transitions/state_transitions.sum()

        idx = state_transitions.cumsum().searchsorted(r)
        return state_transitions.index[idx]




