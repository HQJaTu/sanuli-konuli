#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
import pickle
import random
from typing import Tuple
import logging

log = logging.getLogger(__name__)


def _setup_logger(use_debug: bool) -> None:
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] [%(name)s]  %(message)s")
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(log_formatter)
    console_handler.propagate = False
    log = logging.getLogger()
    log.addHandler(console_handler)
    if use_debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


def load_5_letter_words(words_file: str) -> Tuple[str, str, str, list]:
    with open(words_file, "rb") as pick:
        wordlist_name, alphabet, unwanted_initial_letters, words = pickle.load(pick)

    log.debug("Loaded {} words from {}".format(len(words), wordlist_name))

    return wordlist_name, alphabet, unwanted_initial_letters, words


def match_word(alphabet: str, words: list, mask: str, excluded: str, mandatory: str) -> None:
    known_letters = list(mask.lower())
    excluded_letters = set(list(excluded))
    mandatory_letters = list(mandatory.lower())
    mask_letter_positions = []
    mask_letter_cnt = 0
    mandatory_letter_positions = []
    mandatory_letter_cnt = 0
    for idx in range(5):
        index_processed = False
        if known_letters[idx] in alphabet:
            mask_letter_positions.append(idx)
            index_processed = True
            mask_letter_cnt += 1
        else:
            known_letters[idx] = None
        if mandatory_letters[idx] in alphabet:
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
    for word in words:
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
        for word in prime_matching_words:
            print(word)
        log.info("Found {} (total {}) words with letters '{}'".format(
            len(prime_matching_words), len(matching_words), mandatory
        ))
        random_word = random.choice(prime_matching_words)
    else:
        for word in matching_words:
            print(word)
        log.info("Found {} words with letters '{}'".format(len(matching_words), mandatory))
        random_word = random.choice(matching_words)

    log.info("Random word is: {}".format(random_word))


def main() -> None:
    parser = argparse.ArgumentParser(description='Sanuli matching word finder')
    parser.add_argument('words_file', metavar="PROCESSED-WORDS-DAT-FILE",
                        help="Processed 5-letter words file.")
    parser.add_argument('match_mask', metavar="MATCH-MASK",
                        help="5-letter match mask of known letters")
    parser.add_argument('excluded_letters', metavar="EXCLUDED-LETTERS",
                        help="Set of letters the word must not have")
    parser.add_argument('known_letters', metavar="KNOWN-LETTERS", nargs="?",
                        help="List of letters word must have")
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    if not os.path.exists(args.words_file):
        log.error("Invalid filename '{}'!".format(args.words_file))
        exit(2)

    if len(args.match_mask) != 5:
        log.error("Bad match mask '{}'".format(args.match_mask))
        exit(2)
    if len(args.known_letters) != 5:
        log.error("Bad set of known letters '{}'".format(args.known_letters))
        exit(2)

    log.info("Load pre-saved words from {}".format(args.words_file))
    wordlist_name, alphabet, _, words = load_5_letter_words(args.words_file)
    match_word(alphabet, words, args.match_mask, args.excluded_letters, args.known_letters)
    log.info("Done matching.")


if __name__ == '__main__':
    main()
