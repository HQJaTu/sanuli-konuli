# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import pickle
from abc import abstractmethod
from typing import Tuple, Union
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
        self.word_len = 5

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
        unwanted_letters = list(self.unwanted_initial_letters)
        if excluded:
            excluded_letters = list(excluded)
            attempt = unwanted_letters.copy()
            attempt.extend(excluded_letters)
            initial_words = self._initial_words(attempt)
            if not initial_words:
                # 2nd try without bad letters
                initial_words = self._initial_words(excluded_letters)
        else:
            initial_words = self._initial_words(unwanted_letters)

        initial = random.choice(initial_words)

        return initial

    def _initial_words(self, excluded: list) -> list:
        initial_words = []
        bad_letters = set(excluded)

        for word in self.words:
            word_letters = list(word)
            if bad_letters & set(word_letters):
                continue

            letters = set(word_letters)
            if len(letters) == len(word_letters):
                # Word contains only unique letters
                initial_words.append(word)

        # print(initial_words)
        log.debug("Loaded {} initial words".format(len(initial_words)))

        return initial_words

    def match_word(self, mask: str, excluded: str, mandatory: str) -> Union[str, None]:
        known_letters = list(mask.lower())
        excluded_letters = list(excluded)
        mandatory_letters = list(mandatory.lower())
        matching_words = self._do_match_word(known_letters, excluded_letters, mandatory_letters)
        if not matching_words:
            log.warning("No words matched!")

            return None

        for word in matching_words:
            print(word)

        random_word = random.choice(matching_words)

        log.info("Random word is: {}".format(random_word))

        return random_word

    def _do_match_word(self, known_letters: list, excluded: list, mandatory_letters: list) -> list:
        if len(known_letters) != self.word_len:
            raise ValueError("Mask must be {} characters!".format(self.word_len))
        if len(mandatory_letters) != self.word_len:
            raise ValueError("Mandatory must be {} characters!".format(self.word_len))

        excluded_letters = set(excluded)
        if set(mandatory_letters) & excluded_letters:
            raise ValueError("Excluded letters must not exist in mandatory ones!")

        mask = ''.join([l if l else '.' for l in known_letters])
        mandatory = ''.join([l if l else '.' for l in mandatory_letters])
        mask_letter_positions = []
        mask_letter_cnt = 0
        mandatory_letter_positions = []
        mandatory_letter_cnt = 0
        for idx in range(self.word_len):
            index_processed = False
            if known_letters[idx] in self.alphabet:
                mask_letter_positions.append(idx)
                index_processed = True
                mask_letter_cnt += 1
            else:
                known_letters[idx] = None
            if mandatory_letters[idx] in self.alphabet:
                if index_processed:
                    log.error("Invalid arguments! Mandatory letter '{}' at position {} clashes with known letter '{}'".format(
                        mandatory_letters[idx], idx, known_letters[idx]
                    ))
                    raise ValueError("Mask and mandatory conflict at {}".format(idx))
                mandatory_letter_positions.append(idx)
                mandatory_letter_cnt += 1
            else:
                mandatory_letters[idx] = None

        # Find initial set of potential words based on mask letters
        potential_words = []
        unique_potential_words = set()
        for word in self.words:
            word = word.lower()
            word_matches = True  # By default, word matches
            unmasked_letters_in_this_word = set()
            for idx in range(self.word_len):
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

            # Remaining letters after mask should be unique to maximize attempt footprint.
            if len(unmasked_letters_in_this_word) == self.word_len - mask_letter_cnt:
                unique_potential_words.add(word)

            if word_matches:
                potential_words.append(word)
                # print(word)

        log.info("Found {} potential words with mask '{}'".format(len(potential_words), mask))

        # Reduce list further by adding mandatory letters we know are in the word, but we don't know where.
        # One important thing: We KNOW it is NOT in the given position.
        matching_words = set()
        prime_matching_words = set()
        for word in potential_words:
            word = str(word)
            known_positions = mask_letter_positions.copy()
            added_letters = set()
            letter_match_cnt = 0
            word_is_invalid = False
            if mandatory_letter_positions:
                for letter_pos in mandatory_letter_positions:
                    letter = mandatory_letters[letter_pos]
                    for idx in range(self.word_len):
                        if idx == letter_pos:
                            # We know, this letter is in the word, but not in this position.
                            # Some other position will do the trick
                            if letter == word[idx]:
                                word_is_invalid = True
                                break
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

                    if word_is_invalid:
                        # We figured this word to be very bad. Stop iterating
                        break
                # After all the matching, see how it went
                if not word_is_invalid and letter_match_cnt == mandatory_letter_cnt:
                    matching_words.add(word)
                    # print(word)
                    log.debug("{}, match cnt: {}, len: {}".format(word, letter_match_cnt, len(added_letters)))
                    if len(added_letters) == letter_match_cnt:
                        prime_matching_words.add(word)
            else:
                # No mandatory letters at all
                for idx in range(self.word_len):
                    if idx in mask_letter_positions:
                        # Won't place a mandatory letter on a known letter position
                        continue
                    letter = word[idx]
                    added_letters.add(letter)

                # All words are matches
                matching_words.add(word)
                # print(word)
                log.debug("{}, len: {}/{}".format(word, len(added_letters), mandatory_letter_cnt))
                if len(added_letters) == self.word_len - mask_letter_cnt:
                    prime_matching_words.add(word)

        if prime_matching_words:
            even_primer_matching_words = unique_potential_words & set(prime_matching_words)
            if even_primer_matching_words:
                prime_matching_words = even_primer_matching_words
            # These words have more quality as they maximize footprint
            log.info("Found {} (total {}) words with letters '{}'".format(
                len(prime_matching_words), len(matching_words), mandatory
            ))
            return sorted(list(prime_matching_words))

        # These words don't maximize footprint, but are still valid ones
        log.info("Found {} words with letters '{}'".format(len(matching_words), mandatory))

        return sorted(list(matching_words))
