#!/usr/bin/env python3

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

import os
import sys
import argparse
import pickle
from lxml import etree  # lxml implements the ElementTree API, has better performance or more advanced features
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


def import_words(xml_filename: str) -> list:
    words = []
    with open(xml_filename, "rb") as fp:
        context = etree.iterparse(fp, events=('end',))
        for action, elem in context:
            if elem.tag != 's':
                continue

            if len(elem.text) != 5 or " " in elem.text or "-" in elem.text:
                continue

            words.append(elem.text)
            log.debug(elem.text)

    log.debug("Added {} words".format(len(words)))

    return words


def save_words(words: list, output_file: str) -> None:
    with open(output_file, "wb") as pick:
        kotus_alphabet = 'abcdefghijklmnopqrstuvxyzåäö'
        kotus_unwanted_initial_letters = "bcdfgqwxzöäå"
        data = ('Kotus', kotus_alphabet, kotus_unwanted_initial_letters, words)
        pickle.dump(data, pick)

    log.info("Saved wordlist into {}".format(output_file))


def main() -> None:
    parser = argparse.ArgumentParser(description='Kotus word-list converter')
    parser.add_argument('kotus_word_file', metavar="KOTUS-SANALISTA-V1-XML-FILE",
                        help='Finnish wordlist')
    parser.add_argument('--output-file', default=KOTUS_WORDFILE,
                        help="Processed 5-letter words file. Default: {}".format(KOTUS_WORDFILE))
    parser.add_argument('--debug', action="store_true", default=False,
                        help="Make logging use DEBUG instead of default INFO.")

    args = parser.parse_args()
    _setup_logger(args.debug)

    if not os.path.exists(args.kotus_word_file):
        log.error("Invalid filename '{}'!".format(args.kotus_word_file))
        exit(2)

    log.info("Begin reading {}".format(args.kotus_word_file))
    words = import_words(args.kotus_word_file)
    save_words(words, args.output_file)
    log.info("Done.")


if __name__ == '__main__':
    main()
