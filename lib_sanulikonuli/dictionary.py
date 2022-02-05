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
        initial_words = self._initial_words(excluded)
        initial = random.choice(initial_words)

        return initial

    def _initial_words(self, excluded: str = None) -> list:
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

        return initial_words

    def match_word(self, mask: str, excluded: str, mandatory: str) -> str:
        matching_words = self._do_match_word(mask, excluded, mandatory)
        for word in matching_words:
            print(word)

        random_word = random.choice(matching_words)

        log.info("Random word is: {}".format(random_word))

        return random_word

    def _do_match_word(self, mask: str, excluded: str, mandatory: str) -> list:
        if len(mask) != 5:
            raise ValueError("Mask must be 5 characters!")
        if len(mandatory) != 5:
            raise ValueError("Mandatory must be 5 characters!")

        known_letters = list(mask.lower())
        excluded_letters = set(list(excluded))
        mandatory_letters = list(mandatory.lower())
        mask_letter_positions = []
        mask_letter_cnt = 0
        mandatory_letter_positions = []
        mandatory_letter_cnt = 0
        for idx in range(5):
            index_processed = False
            if known_letters[idx] in self.alphabet:
                mask_letter_positions.append(idx)
                index_processed = True
                mask_letter_cnt += 1
            else:
                known_letters[idx] = None
            if mandatory_letters[idx] in self.alphabet:
                if index_processed:
                    log.error("Mandatory letter '{}' at position {} clashes with known letter '{}'".format(
                        idx, mandatory_letters[idx], known_letters[idx]
                    ))
                    raise ValueError
                mandatory_letter_positions.append(idx)
                mandatory_letter_cnt += 1
            else:
                mandatory_letters[idx] = None

        # Find initial set of potential words based on mask letters
        potential_words = []
        for word in self.words:
            word = word.lower()
            word_matches = True  # By default, word matches
            unmasked_letters_in_this_word = set()
            for idx in range(5):
                if idx in mask_letter_positions:
                    if word[idx] != known_letters[idx]:
                        word_matches = False
                        break
                else:
                    unmasked_letters_in_this_word.add(word[idx])

            if not word_matches:
                continue

            # Non-masked letters must not contain any of the excluded
            if unmasked_letters_in_this_word & excluded_letters:
                # This word contains excluded letters
                continue

            if word_matches:
                potential_words.append(word)
                # print(word)

        log.info("Found {} potential words with mask '{}'".format(len(potential_words), mask))

        # Reduce list further
        matching_words = []
        prime_matching_words = []
        for word in potential_words:
            word = str(word)
            known_positions = mask_letter_positions.copy()
            added_letters = set()
            letter_match_cnt = 0
            if mandatory_letter_positions:
                for letter_pos in mandatory_letter_positions:
                    letter = mandatory_letters[letter_pos]
                    for idx in range(5):
                        if idx == letter_pos:
                            # We know, this letter is in the word, but not in this position.
                            # Some other position will do the trick
                            continue
                        if idx in mask_letter_positions:
                            # Won't place a mandatory letter on a known letter position
                            continue
                        if letter == word[idx]:
                            # A potential match.
                            # This word has a mandatory letter in different position.
                            known_positions.append(idx)
                            added_letters.add(letter)
                            letter_match_cnt += 1
                            break
                # After all the matching, see how it went
                if letter_match_cnt == mandatory_letter_cnt:
                    matching_words.append(word)
                    # print(word)
                    log.debug("{}, match cnt: {}, len: {}".format(word, letter_match_cnt, len(added_letters)))
                    if len(added_letters) == letter_match_cnt:
                        prime_matching_words.append(word)
            else:
                # No mandatory letters at all
                for idx in range(5):
                    if idx in mask_letter_positions:
                        # Won't place a mandatory letter on a known letter position
                        continue
                    letter = word[idx]
                    added_letters.add(letter)

                # All words are matches
                matching_words.append(word)
                # print(word)
                log.debug("{}, len: {}/{}".format(word, len(added_letters), mandatory_letter_cnt))
                if len(added_letters) == 5 - mask_letter_cnt:
                    prime_matching_words.append(word)

        if prime_matching_words:
            # These words have more quality as they maximize footprint
            log.info("Found {} (total {}) words with letters '{}'".format(
                len(prime_matching_words), len(matching_words), mandatory
            ))
            return prime_matching_words

        # These words don't maximize footprint, but are still valid ones
        log.info("Found {} words with letters '{}'".format(len(matching_words), mandatory))

        return matching_words
