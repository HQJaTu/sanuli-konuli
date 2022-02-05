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
        words = self.dictionary._do_match_word('.....', '', '.....')
        self.assertEqual(words, expected_words, "Find with no criteria at all fail")

    def test_one_mask_letter(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = ['aamen', 'ahven', 'ameba', 'asema', 'asemo', 'aueta']
        words = self.dictionary._do_match_word('a....', '', '.....')
        self.assertEqual(words, expected_words, "Find with one criteria fail")

    def test_two_mask_letters(self):
        # This is a set of prime words to maximize the attempt footprint
        expected_words = ['asema', 'asemo']
        words = self.dictionary._do_match_word('as...', '', '.....')
        self.assertEqual(words, expected_words, "Find with two criteria fail")
