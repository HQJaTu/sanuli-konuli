from lxml import etree  # lxml implements the ElementTree API, has better performance or more advanced features
import logging
from ..dictionary import Dictionary

log = logging.getLogger(__name__)


class KotusDictionary(Dictionary):

    def __init__(self):
        super().__init__("Kotus", 'abcdefghijklmnopqrstuvxyzåäö', "bcdfgqwxzöäå")

    def import_words(self, number_of_letters: int, xml_filename: str) -> list:
        self.word_len = number_of_letters
        self.words = []
        alphabet = set(list(self.alphabet))
        with open(xml_filename, "rb") as fp:
            context = etree.iterparse(fp, events=('end',))
            for action, elem in context:
                if elem.tag != 's':
                    continue

                if len(elem.text) != self.word_len:
                    continue

                characters = set(list(elem.text.lower()))
                if characters - alphabet:
                    # Not all characters are in alphabet. Skip this.
                    continue

                self.words.append(elem.text.lower())
                log.debug("{}-letter word: {}".format(self.word_len, elem.text))

        log.debug("Added {} words".format(len(self.words)))

        return self.words

    def add_word(self, word_to_add: str) -> None:
        if len(word_to_add) != self.word_len:
            raise ValueError("Word '{}' doesn't match length of {}!".format(word_to_add, self.word_len))

        alphabet = set(list(self.alphabet))
        characters = set(list(word_to_add.lower()))
        if characters - alphabet:
            # Not all characters are in alphabet. Skip this.
            raise ValueError("Word '{}' doesn't match alphabet of this dictionary!".format(word_to_add))

        self.words.append(word_to_add.lower())
        log.debug("{}-letter word: {}".format(self.word_len, word_to_add))
