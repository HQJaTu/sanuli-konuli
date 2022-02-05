from testsetup import DictionaryTestBase


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
