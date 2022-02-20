import os
from typing import Union
from django.conf import settings
from lib_sanulikonuli import Dictionary


class DictionaryLoader:
    my_dicts = {}

    @staticmethod
    def load(language: str, word_length: int) -> Union[None, Dictionary]:
        if not DictionaryLoader.my_dicts:
            DictionaryLoader.my_dicts = DictionaryLoader._parse_dictionaries()

        if language not in DictionaryLoader.my_dicts:
            return None
        if word_length not in DictionaryLoader.my_dicts[language]:
            return None

        path = DictionaryLoader.my_dicts[language][word_length]

        words = Dictionary()
        words.load_words(path)

        return words

    @staticmethod
    def _parse_dictionaries() -> dict:
        #dicts = settings["DICTIONARIES"].split(',')
        dicts = settings.DICTIONARIES
        dicts_out = {}
        for dictionary_data in dicts:
            parts = dictionary_data.split(':', 3)
            lang = parts[0]
            word_length = int(parts[1])
            if not os.path.exists(parts[2]):
                raise ValueError("Given dictionary '{}' does not exist!".format(dictionary_data))
            path = parts[2]

            if lang in dicts_out:
                if word_length in dicts_out[lang]:
                    raise ValueError("Language '{}' has word length {} twice!".format(lang, word_length))
                dicts_out[lang][word_length] = path
            else:
                dicts_out[lang] = {
                    word_length: path
                }

        return dicts_out
