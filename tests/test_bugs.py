from .testsetup import DictionaryTestBase


class TestBugs(DictionaryTestBase):
    def setUp(self):
        super().setUp()
        self.dictionary.words = [
            'bussi', 'fusku', 'hissi', 'höskä', 'inssi', 'jussi', 'kuski', 'kyssä',
            'kystä', 'kysyä', 'käsin', 'käsky', 'käsnä', 'kössi', 'kössi', 'lisää',
            'lysti', 'läsiä', 'läski', 'läsnä', 'lässy', 'lössi', 'lössi', 'missi',
            'missä', 'mistä', 'mussu', 'myski', 'mysli', 'myssy', 'mäsis', 'mäski',
            'mössö', 'nisti', 'nysty', 'näsiä', 'nössö', 'pisiä', 'piski', 'pissi',
            'pusku', 'pussi', 'pyssy', 'pysti', 'pysty', 'pystö', 'pysyä', 'pässi',
            'riski', 'riski', 'risti', 'ryssä', 'rysty', 'rästi', 'rösti', 'sisin',
            'sissi', 'sisus', 'sussu', 'sysiä', 'sössö', 'tiski', 'tissi', 'tussi',
            'tussu', 'tässä', 'tästä', 'unssi', 'upsis', 'yksin', 'yksiö', 'äiskä',
            'öisin',
        ]

    def test_incorrect_mandatory(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = []
        words = self.dictionary._do_match_word(list("l.s.ä"), 'veoakysi', list(".ä..."))
        self.assertEqual(expected_words, words, "Find with no criteria at all fail")

    def test_correct_mandatory(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = ['läsnä']
        words = self.dictionary._do_match_word(list("l.s.ä"), 'veoakysi', list("...ä."))
        self.assertEqual(expected_words, words, "Find with no criteria at all fail")
