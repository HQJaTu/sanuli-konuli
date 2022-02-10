from .testsetup import DictionaryTestBase


class TestBugs(DictionaryTestBase):

    def _setup_test_dictionary_1(self):
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
        self._setup_test_dictionary_1()
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list("l.s.ä"), 'veoakysi', list(".ä..."))
        self.assertEqual(expected_words, words, "Finding from given set fails")
        self.assertEqual(None, prime_words, "Finding from given set fails")

    def test_correct_mandatory(self):
        self._setup_test_dictionary_1()
        expected_prime = ['läsnä']
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list("l.s.ä"), 'veoakysi', list("...ä."))
        self.assertEqual(expected_words, words, "Finding from given set fails")
        self.assertEqual(expected_prime, prime_words, "Finding from given set fails")

    def _setup_test_dictionary_2(self):
        self.dictionary.words = [
            'naama', 'naara', 'naava', 'nahas', 'nahka', 'nanna', 'nappa', 'nassu',
            'nauha', 'naula', 'nauru', 'nugaa', 'nukka', 'nulju', 'nunna', 'nuppu',
            'nuuka', 'nykyä', 'nylky', 'nynny', 'nyppy', 'nähdä', 'näkyä', 'nälkä',
            'näppy', 'näpsä', 'nössö', 'naksu', 'napsu', 'nurja', 'nöyrä', 'nykyä',
            'nylky', 'nynny', 'nyppy', 'nähdä', 'näkyä', 'nälkä', 'näppy', 'näpsä',
            'nössö',
        ]

    def test_conflicting_mandatory_and_exclude(self):
        self._setup_test_dictionary_2()
        expected_prime = ['näppy']
        expected_words = []
        words, prime_words = self.dictionary._do_match_word(list("n...."), 'eitourjaky', list(".y..ä"))
        self.assertEqual(expected_words, words, "Finding from given set fails")
        self.assertEqual(expected_prime, prime_words, "Finding from given set fails")

    def _setup_test_dictionary_3(self):
        self.dictionary.words = ['ajaja', 'akana', 'ammua', 'ankka', 'anoja', 'asuja', 'asuma', 'aukoa', 'baana',
                                 'bygga', 'fauna', 'fokka', 'fuuga', 'gamma', 'hanka', 'hansa', 'hohka', 'homma',
                                 'honka', 'hosua', 'hukka', 'humma', 'huuma', 'jaaha', 'jahka', 'jakaa', 'jooga',
                                 'jukka', 'juoma', 'kakka', 'kanna', 'kanna', 'kansa', 'kassa', 'kauha', 'kauna',
                                 'kokka', 'konna', 'konsa', 'kooma', 'koska', 'kukka', 'kuksa', 'kumma', 'kuoha',
                                 'kuoma', 'kuona', 'kussa', 'kuuma', 'magma', 'magna', 'maksa', 'mamba', 'mamma',
                                 'manna', 'massa', 'mokka', 'mokka', 'moska', 'mukaa', 'muona', 'muusa', 'naama',
                                 'nahka', 'nanna', 'nauha', 'nokka', 'nugaa', 'nukka', 'nunna', 'nuuka', 'osuma',
                                 'saaga', 'saaja', 'safka', 'sakka', 'saksa', 'samba', 'sanka', 'sanoa', 'sauma',
                                 'sauna', 'sokka', 'sooma', 'sujua', 'sukka', 'summa', 'sunna', 'suoja', 'suoja',
                                 'suoja', 'uhkua', 'uskoa']

    def test_single_words_returned(self):
        self._setup_test_dictionary_3()
        expected_prime = ['mukaa']
        expected_words = ['ammua']
        words, prime_words = self.dictionary._do_match_word(list("....a"), 'trvepidl', list(".aum."))
        self.assertEqual(expected_words, words, "Finding from given set fails")
        self.assertEqual(expected_prime, prime_words, "Finding from given set fails")
