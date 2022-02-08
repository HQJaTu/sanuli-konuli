from .testsetup import DictionaryTestBase


class TestFindWord(DictionaryTestBase):

    def test_no_mask_letters(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = ['aamen',
                          'ameba',
                          'asema',
                          'asete',
                          'aueta',
                          'bebee',
                          'beeta',
                          'debet',
                          'edetä',
                          'eeden',
                          'eheys',
                          'ehtoo',
                          'enetä',
                          'ennen',
                          'entää',
                          'eroon',
                          'essee',
                          'estää',
                          'etana',
                          'eteen',
                          'etevä',
                          'etuus',
                          'evätä',
                          'genre',
                          'getto']
        expected_prime = ['ahven',
                          'asemo',
                          'bensa',
                          'bänet',
                          'ehtyä',
                          'entäs',
                          'erota',
                          'estyä',
                          'heavy',
                          'hefta']
        words, prime_words = self.dictionary._do_match_word(list('.....'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with no criteria at all fail")
        self.assertEqual(expected_prime, prime_words, "Find with no criteria at all fail")

    def test_one_mask_letter(self):
        # First letter of the word must have letter 'a' first
        expected_prime = ['aamen', 'ahven', 'ameba', 'asema', 'asemo', 'aueta']
        expected_words = ['asete']
        words, prime_words = self.dictionary._do_match_word(list('a....'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask letter fail")

    def test_negative_one_mask_letter(self):
        # First letter of the word must have letter 'x' first
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list('x....'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(None, prime_words, "Find with one mask letter fail")

    def test_two_mask_letters(self):
        # First two letter of the word must have letters 'a' and 's'
        expected_prime = ['asema', 'asemo']
        expected_words = ['asete']
        words, prime_words = self.dictionary._do_match_word(list('as...'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with two mask letters fail")
        self.assertEqual(expected_prime, prime_words, "Find with two mask letters fail")

    def test_three_mask_letters(self):
        # First letter of the word must have letter 'e', third letter 'e' and fourth letter 't'
        expected_prime = ['edetä', 'enetä']
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list('e.et.'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with three mask letters fail")
        self.assertEqual(expected_prime, prime_words, "Find with three mask letters fail")

    def test_one_mandatory_letter(self):
        # There is a letter 'e' in the word. We know it is not the first, mask is empty.
        expected_prime = [  # 'aamen',
            'ahven',
            # 'ameba',
            # 'asema',
            'asemo',
            # 'asete',
            # 'aueta',
            # 'bebee',
            # 'beeta',
            'bensa',
            'bänet',
            # 'debet',
            # 'genre',
            # 'getto',
            'heavy',
            'hefta']
        expected_words = ['aamen',
                          'ameba',
                          'asema',
                          'asete',
                          'aueta',
                          'bebee',
                          'beeta',
                          'debet',
                          'genre',
                          'getto']
        words, prime_words = self.dictionary._do_match_word(list('.....'), '', list('e....'))
        self.assertEqual(expected_words, words, "Find with one mandatory letters fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mandatory letters fail")

    def test_two_mandatory_letters(self):
        # There is a letter 'e' in the word. We know it is not the first, mask is empty.
        # There is a letter 'n' in the word. We know it is not the third, mask is empty.
        expected_prime = [  # 'aamen',
            'ahven'
        ]
        expected_words = ['aamen']
        words, prime_words = self.dictionary._do_match_word(list('.....'), '', list('e.n..'))
        self.assertEqual(expected_words, words, "Find with two mandatory letters fail")
        self.assertEqual(expected_prime, prime_words, "Find with two mandatory letters fail")

    def test_one_mask_and_one_mandatory_letter(self):
        expected_prime = ['ahven']
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list('.h...'), '', list('e.n..'))
        self.assertEqual(expected_words, words, "Find with one mask and one mandatory letters fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask and one mandatory letters fail")

    def test_one_exclude_letter(self):
        # There is no letter 'a' in the word at all.
        expected_prime = ['bänet', 'ehtyä', 'entäs', 'estyä']
        expected_words = ['bebee',
                          'debet',
                          'edetä',
                          'eeden',
                          'eheys',
                          'ehtoo',
                          'enetä',
                          'ennen',
                          'entää',
                          'eroon',
                          'essee',
                          'estää',
                          'eteen',
                          'etevä',
                          'etuus',
                          'evätä',
                          'genre',
                          'getto']
        words, prime_words = self.dictionary._do_match_word(list('.....'), 'a', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask letter fail")

    def test_one_mask_and_one_exclude_letter(self):
        # We know first letter of the word is 'e' and and there is no letter 't' anywhere else.
        expected_prime = ['eheys']
        expected_words = ['eeden', 'ennen', 'eroon', 'essee']
        words, prime_words = self.dictionary._do_match_word(list('e....'), 't', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask letter fail")

    def test_one_mask_and_matching_exclude_letter(self):
        # We know first letter of the word is 'e' and and there is no letter 'e' anywhere else.
        expected_prime = ['ehtyä', 'entäs', 'erota', 'estyä']
        expected_words = ['ehtoo', 'entää', 'eroon', 'estää', 'etana', 'etuus', 'evätä']
        words, prime_words = self.dictionary._do_match_word(list('e....'), 'e', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask letter fail")
