#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
import logging
from lib_sanulikonuli import Dictionary

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
    words = Dictionary()
    words.load_5_letter_words(args.words_file)
    words.match_word(args.match_mask, args.excluded_letters, args.known_letters)
    log.info("Done matching.")


if __name__ == '__main__':
    main()
