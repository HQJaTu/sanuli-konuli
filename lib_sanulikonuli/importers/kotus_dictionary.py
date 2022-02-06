from lxml import etree  # lxml implements the ElementTree API, has better performance or more advanced features
import logging
from ..dictionary import Dictionary

log = logging.getLogger(__name__)


class KotusDictionary(Dictionary):

    def __init__(self):
        super().__init__("Kotus", 'abcdefghijklmnopqrstuvxyzåäö', "bcdfgqwxzöäå")

    def import_words(self, xml_filename: str) -> list:
        self.words = []
        with open(xml_filename, "rb") as fp:
            context = etree.iterparse(fp, events=('end',))
            for action, elem in context:
                if elem.tag != 's':
                    continue

                if len(elem.text) != 5 or " " in elem.text or "-" in elem.text:
                    continue

                self.words.append(elem.text.lower())
                log.debug(elem.text)

        log.debug("Added {} words".format(len(self.words)))

        return self.words
