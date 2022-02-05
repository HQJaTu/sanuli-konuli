from testsetup import DictionaryTestBase


class TestFindWord(DictionaryTestBase):

    def test_no_mask_letters(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = ['ahven',
                          'asemo',
                          'bensa',
                          'bänet',
                          'ehtyä',
                          'entäs',
                          'erota',
                          'estyä',
                          'heavy',
                          'hefta']
        words = self.dictionary._do_match_word(list('.....'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with no criteria at all fail")

    def test_one_mask_letter(self):
        # First letter of the word must have letter 'a' first
        expected_words = ['aamen', 'ahven', 'ameba', 'asema', 'asemo', 'aueta']
        words = self.dictionary._do_match_word(list('a....'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")

    def test_two_mask_letters(self):
        # First two letter of the word must have letters 'a' and 's'
        expected_words = ['asema', 'asemo']
        words = self.dictionary._do_match_word(list('as...'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with two mask letters fail")

    def test_three_mask_letters(self):
        # First letter of the word must have letter 'e', third letter 'e' and fourth letter 't'
        expected_words = ['edetä', 'enetä']
        words = self.dictionary._do_match_word(list('e.et.'), '', list('.....'))
        self.assertEqual(expected_words, words, "Find with three mask letters fail")

    def test_one_mandatory_letter(self):
        # There is a letter 'e' in the word. We know it is not the first, mask is empty.
        expected_words = ['aamen',
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
                          'genre',
                          'getto',
                          'heavy',
                          'hefta']
        words = self.dictionary._do_match_word(list('.....'), '', list('e....'))
        self.assertEqual(expected_words, words, "Find with one mandatory letters fail")
