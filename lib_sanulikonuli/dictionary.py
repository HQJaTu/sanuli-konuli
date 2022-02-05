# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import pickle
from abc import abstractmethod
from typing import Tuple
import random
import logging

log = logging.getLogger(__name__)


class Dictionary:

    def __init__(self, name: str = None, alphabet: str = None, unwanted_initial_letters: str = None):
        """
        Base class for a dictionary
        :param name: Name of this dictionary
        :param alphabet: alphabet to use for determining word characters
        :param unwanted_initial_letters: set of "rare" letters not used in initial word selection
        """
        self.name = name
        self.words = None
        self.alphabet = alphabet
        self.unwanted_initial_letters = unwanted_initial_letters

    @abstractmethod
    def import_words(self, xml_filename: str) -> list:
        pass

    def save_words(self, output_file: str) -> None:
        with open(output_file, "wb") as pick:
            data = (self.name, self.alphabet, self.unwanted_initial_letters, self.words)
            pickle.dump(data, pick)

        log.info("Saved wordlist into {}".format(output_file))

    def load_5_letter_words(self, words_file: str) -> Tuple[str, str, str, list]:
        with open(words_file, "rb") as pick:
            wordlist_name, alphabet, unwanted_initial_letters, words = pickle.load(pick)

        self.name = wordlist_name
        self.alphabet = alphabet
        self.unwanted_initial_letters = unwanted_initial_letters
        self.words = words
        log.debug("Loaded {} words from {}".format(len(self.words), wordlist_name))

        return wordlist_name, alphabet, unwanted_initial_letters, words

    def select_random_initial_word(self, excluded: str = None) -> str:
        initial_words = []
        bad_letters = set(list(self.unwanted_initial_letters))
        if excluded:
            excluded_letters = set(list(excluded))
        else:
            excluded_letters = set()

        for word in self.words:
            word_letters = list(word)
            if bad_letters & set(word_letters):
                continue
            if excluded_letters & set(word_letters):
                continue

            letters = set()
            word_is_ok = True
            for letter in word_letters:
                if letter in letters:
                    word_is_ok = False
                    break
                letters.add(letter)

            if word_is_ok:
                initial_words.append(word)

        # print(initial_words)
        log.debug("Loaded {} initial words".format(len(initial_words)))

        initial = random.choice(initial_words)

        return initial
