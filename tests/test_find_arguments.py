from testsetup import DictionaryTestBase


class TestFindArguments(DictionaryTestBase):

    def test_mask_argument(self):
        # Invalid mask
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word('....', '', '.....')

        self.assertTrue('Mask must be 5 characters!' in str(context.exception))

        # Invalid mandatory
        with self.assertRaises(ValueError) as context:
            self.dictionary._do_match_word('.....', '', '....')

        self.assertTrue('Mandatory must be 5 characters!' in str(context.exception))
