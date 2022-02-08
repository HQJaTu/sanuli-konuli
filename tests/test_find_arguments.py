from .testsetup import DictionaryTestBase


class TestFindArguments(DictionaryTestBase):

    def test_mask_argument(self):
        # Invalid mask
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word('....', '', '.....')

        self.assertTrue('Mask must be 5 characters!' in str(context.exception))

    def test_mandatory_argument(self):
        # Invalid mandatory
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word('.....', '', '....')

        self.assertTrue('Mandatory must be 5 characters!' in str(context.exception))

    def test_conflicting_mask_and_mandatory_arguments(self):
        # Both values are valid, but conflict.
        # Same position cannot have both mask and mandatory letter.
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word('a....', '', 'e....')

        self.assertTrue('Mask and mandatory conflict at 0' in str(context.exception))

    def test_conflicting_exclude_and_mandatory_arguments(self):
        # Both values are valid, but conflict.
        # Cannot exclude a mandatory letter.
        # In this example we know letter 'e' is not the first letter of the word, but as we exclude it completely
        # there is no way of determining at which location it is at.
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word(list('.....'), 'e', list('e....'))

        self.assertTrue('Excluded letters must not exist in mandatory ones!' in str(context.exception))

    def test_conflicting_exclude_and_mask_arguments(self):
        # Both values are valid, conflict, but this is ok.
        # In this example we know letter 'e' is the first letter of the word and no other can be 'e'.
        # Ref.: see test_one_mask_and_matching_exclude_letter()
        expected_prime = ['ehtyä', 'entäs', 'erota', 'estyä']
        expected_words = ['ehtoo', 'entää', 'eroon', 'estää', 'etana', 'etuus', 'evätä']
        words, prime_words = self.dictionary._do_match_word(list('e....'), 'e', list('.....'))
        self.assertEqual(expected_words, words, "Find with one mask letter fail")
        self.assertEqual(expected_prime, prime_words, "Find with one mask letter fail")
