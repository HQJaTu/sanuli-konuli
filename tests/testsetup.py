from unittest import TestCase
from lib_sanulikonuli import Dictionary


class DictionaryTestBase(TestCase):
    def setUp(self):
        self.dictionary = Dictionary('TestDict', 'abcdefghijklmnopqrstuvxyzåäö', "bcdfgqwxzöäå")
        self.dictionary.words = [
            'aamen',
            'ahven',
            'ameba',
            'asema',
            'asemo',
            'asete',
            'aueta',
            'bebee',
            'beeta',
            'bensa',
            'bänet',
            'debet',
            'edetä',
            'eeden',
            'eheys',
            'ehtoo',
            'ehtyä',
            'enetä',
            'ennen',
            'entäs',
            'entää',
            'eroon',
            'erota',
            'essee',
            'estyä',
            'estää',
            'etana',
            'eteen',
            'etevä',
            'etuus',
            'evätä',
            'genre',
            'getto',
            'heavy',
            'hefta',
        ]
