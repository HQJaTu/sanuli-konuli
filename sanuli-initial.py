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


def select_random_initial_word(unwanted_letters: str, words: list, excluded: str) -> str:
    initial_words = []
    bad_letters = set(list(unwanted_letters))
    if excluded:
        excluded_letters = set(list(excluded))
    else:
        excluded_letters = set()

    for word in words:
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


def main() -> None:
    parser = argparse.ArgumentParser(description='Sanuli initial word')
    parser.add_argument('words_file', metavar="PROCESSED-WORDS-DAT-FILE",
                        help="Processed 5-letter words file.")
    parser.add_argument('excluded_letters', metavar="EXCLUDED-LETTERS", nargs="?",
                        help="Set of letters the word must not have")
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    if not os.path.exists(args.words_file):
        log.error("Invalid filename '{}'!".format(args.words_file))
        exit(2)

    log.info("Load pre-saved words")
    wordlist_name, _, unwanted_initial_letters, words = load_5_letter_words(args.words_file)
    initial = select_random_initial_word(unwanted_initial_letters, words, args.excluded_letters)
    log.info("Initial word is: {}".format(initial))


if __name__ == '__main__':
    main()
