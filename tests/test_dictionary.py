from testsetup import DictionaryTestBase


class TestDictionary(DictionaryTestBase):

    def test_initial_words(self):
        # Get a list of initial words.
        # An initial word has no duplicate letters to maximize footprint.
        # Also initial word has none of the unwanted_initial_letters -list letters.
        words = self.dictionary._initial_words()
        self.assertEqual(words, ['ahven', 'asemo', 'erota', 'heavy'], "Initial words list fail")

    def test_initial_words_with_filter(self):
        # Initial words without letters 'o' and 'y'
        words = self.dictionary._initial_words("oy")
        self.assertEqual(words, ['ahven'], "Initial words list filtering fail")
