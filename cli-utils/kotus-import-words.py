#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
from lib_sanulikonuli.importers.kotus_dictionary import KotusDictionary
import logging

log = logging.getLogger(__name__)

KOTUS_WORDFILE = r'kotus-sanalista_v1.dat'


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
    parser = argparse.ArgumentParser(description='Kotus word-list converter')
    parser.add_argument('kotus_word_file', metavar="KOTUS-SANALISTA-V1-XML-FILE",
                        help='Finnish wordlist')
    parser.add_argument('number_of_letters', metavar="WORD-LENGTH", type=int,
                        help="Number of letters to import from wordlist")
    parser.add_argument('add_word', metavar="ADD-WORD-TO-DICTIONARY", nargs="*", default=None,
                        help="Add a matching word to dictionary. Can have any number of these.")
    parser.add_argument('--output-file', default=KOTUS_WORDFILE,
                        help="Processed wordlist file. Default: {}".format(KOTUS_WORDFILE))
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    if not os.path.exists(args.kotus_word_file):
        log.error("Invalid filename '{}'!".format(args.kotus_word_file))
        exit(2)

    log.info("Begin reading {}".format(args.kotus_word_file))
    words = KotusDictionary()
    words.import_words(args.number_of_letters, args.kotus_word_file)
    if args.add_word:
        for word in args.add_word:
            words.add_word(word)
    words.save_words(args.output_file)
    log.info("Done.")


if __name__ == '__main__':
    main()
