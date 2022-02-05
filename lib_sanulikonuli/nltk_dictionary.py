from nltk import corpus, download as nltk_download
import logging
from .dictionary import Dictionary

log = logging.getLogger(__name__)


class NltkDictionary(Dictionary):
    """
    NLTK is at https://www.nltk.org/
    """
    CORPUS = 'wordnet2021'

    def __init__(self):
        super().__init__("Natural Language Toolkit - {}".format(self.CORPUS),
                         'abcdefghijklmnopqrstuvxyz', "jqxzwvfybh")
        # Least frequent dictionary letters from: https://en.wikipedia.org/wiki/Letter_frequency

        # Prep!
        # NLTK Corpora list: https://www.nltk.org/nltk_data/
        nltk_download('omw-1.4')
        nltk_download('wordnet')
        nltk_download(self.CORPUS)

    def import_words(self, xml_filename: str) -> list:
        self.words = []
        alphabet = set(list(self.alphabet))
        for word in corpus.wordnet2021.words():
            if len(word) != self.word_len:
                continue

            characters = set(list(word))
            if characters - alphabet:
                # Not all characters are in alphabet. Skip this.
                continue

            self.words.append(word.lower())
            log.debug(word)

        log.debug("Added {} words".format(len(self.words)))

        return self.words
