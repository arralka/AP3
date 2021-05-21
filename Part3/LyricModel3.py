from Part2.LyricModel2 import LyricModel2
from helpers.lyric_reader import LyricReader
import requests
import math
import pandas as pd
import numpy as np
import json
from tqdm import tqdm


class LyricModel3(LyricModel2):
    def __init__(self, lyric_reader: LyricReader, n, seed=None, syl_count=None, max_lyrics=None):
        """
        Markov Lyric Model for rhyming and syllables
        """
        with open('output/syllable_dictionary.json') as s:
            self.syllables = pd.Series(json.load(s))
        super().__init__(lyric_reader, n, seed, max_lyrics)

        if syl_count is None:
            self.syl_count = self.calc_avg_syllables()
        else:
            self.syl_count = syl_count

        self.end_states = self.calculate_end_states()

    def get_syllables(self, word):
        syl = max(self.syllables.get(word, 2), 1)
        return syl if syl == syl and syl is not None else 2

    def calculate_end_states(self):
        end_states = self.P['</s>']
        return list(end_states[end_states>0].index)

    def calc_avg_syllables(self):
        syllables = []

        for line in tqdm(self.lyrics, desc='Syllable Calculation'):
            syllables.append(sum([self.get_syllables(w) for w in line.split(' ')[1:-1]]))

        return math.floor(sum(syllables)/len(syllables))

    def _create_line(self, rhyme_constraint=None):
        """
        Creates a single line of lyric
        :return: Randomly generate lyric
        """

        remaining_syllables = self.syl_count

        # Initialise starting state
        seed = ("<s> " * (self.n_count - 1)).strip()
        success = False
        line = seed
        while not success:
            # Get rhyming words
            if rhyme_constraint:
                rhymes = self.get_rhymes(rhyme_constraint)
                if rhymes is None: # If rhyming API query returns nothing get normal word
                    next_word, last_syllable = self._fetch_word_syl(seed, remaining_syllables)
                else:
                    next_word = self._fetch_rhyming_word(seed, rhymes)
                    last_syllable = self.get_syllables(next_word)
            else:
                next_word, last_syllable = self._fetch_word_syl(seed, remaining_syllables)
            # Recursively build line

            line, success = self.recursive_line_creator(f'{seed} {next_word}', remaining_syllables-last_syllable)

        return ' '.join(reversed(line.replace('<s> ', '').replace(' </s>', '').split(' '))).capitalize()

    def _fetch_word_syl(self, state, remaining_syllables):
        r = np.random.rand()
        state_transitions = self.P.loc[state]
        state_transitions = state_transitions.drop('</s>')
        state_transitions = state_transitions[state_transitions > 0]
        state_transitions = self.filter_to_syllables(state_transitions, remaining_syllables, state)

        if len(state_transitions) == 0: # If no words with syllables remaining return None
            return None, None

        # Redistribute probabilities
        state_transitions = state_transitions / state_transitions.sum()

        idx = state_transitions.cumsum().searchsorted(r)
        word = state_transitions.index[idx]
        return word, self.get_syllables(word)

    def filter_to_syllables(self, state_transitions, remaining_syllables, current_state):
        # Filter to words with less syllables than remaining, and equal syllables then remaining but also will reach end state next
        lesser_syllables = [x for x in state_transitions.index if self.get_syllables(x) <= remaining_syllables]
        equal_syllables = [x for x in state_transitions.index if
                           ' '.join(current_state.split(' ')[1:] + [x]) in self.end_states
                           and self.get_syllables(x) == remaining_syllables]

        # Filter to available words
        state_transitions = state_transitions.filter(list(set(lesser_syllables+equal_syllables)))

        # Normalise probabilities (no longer Markovian)
        return state_transitions/state_transitions.sum()

    def recursive_line_creator(self, line, remaining_syllables):
        if remaining_syllables <= 0:
            return line+' </s>', True
        else:
            current_state = ' '.join(line.split(' ')[-(self.n_count - 1):])
            next_word, next_syllables = self._fetch_word_syl(current_state, remaining_syllables)
            original_line = line

            if next_word is None:
                return line, False
            else:
                line, success = self.recursive_line_creator(original_line + ' ' + next_word, remaining_syllables - next_syllables)
                fail_count = 0
                while not success:
                    fail_count += 1
                    next_word, next_syllables = self._fetch_word_syl(current_state, remaining_syllables)
                    line, success = self.recursive_line_creator(original_line + ' ' + next_word, remaining_syllables - next_syllables)
                    if fail_count > 10:
                        return original_line, False
                return line, True

