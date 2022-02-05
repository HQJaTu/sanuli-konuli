from .testsetup import DictionaryTestBase


class TestDictionary(DictionaryTestBase):

    def test_initial_words(self):
        # Get a list of initial words.
        # An initial word has no duplicate letters to maximize footprint.
        # Also initial word has none of the unwanted_initial_letters -list letters.
        unwanted_letters = list(self.dictionary.unwanted_initial_letters)
        words = self.dictionary._initial_words(unwanted_letters)
        self.assertEqual(['ahven', 'asemo', 'erota', 'heavy'], words, "Initial words list fail")

    def test_initial_words_with_filter(self):
        # Initial words without letters 'o' and 'y'
        unwanted_letters = list(self.dictionary.unwanted_initial_letters)
        unwanted_letters.extend(list("oy"))
        words = self.dictionary._initial_words(unwanted_letters)
        self.assertEqual(['ahven'], words, "Initial words list filtering fail")
