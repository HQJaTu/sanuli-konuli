#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
from lib_sanulikonuli.importers.nltk_dictionary import NltkDictionary
import logging

log = logging.getLogger(__name__)

NLTK_WORDFILE = r'nltk-wordnet2021.dat'


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
    parser = argparse.ArgumentParser(description='NLTK word-list converter')
    parser.add_argument('number_of_letters', metavar="WORD-LENGTH", type=int,
                        help="Number of letters to import from wordlist")
    parser.add_argument('--output-file', default=NLTK_WORDFILE,
                        help="Processed wordlist file. Default: {}".format(NLTK_WORDFILE))
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    log.info("Begin")
    words = NltkDictionary()
    words.import_words(args.number_of_letters, "")
    words.save_words(args.output_file)
    log.info("Done.")


if __name__ == '__main__':
    main()
