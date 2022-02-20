from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
import logging
from django.conf import settings
from django.http.response import HttpResponseNotFound
from rest_framework.views import APIView
from ..serializers.v1 import WordsV1Serializer, WordV1Serializer, RequestV1Serializer
from lib_sanulikonuli import Dictionary
from .dictionary_loader import DictionaryLoader

log = logging.getLogger(__name__)


class API(APIView):

    def get_initial(self, request, lang: str, word_length: int, excluded: str = None):
        word_length = int(word_length)
        words = DictionaryLoader.load(lang, word_length)
        initial = words.select_random_initial_word(excluded)
        log.info("Initial word is: {}".format(initial))

        word_data = {
            "word": initial
        }
        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = WordV1Serializer(data=word_data)
        if not serializer.is_valid():
            log.error("Errors: {}".format(serializer.errors))

            return HttpResponseServerError("Data not formatted correctly!")

        return JsonResponse(serializer.validated_data)

    def post_find_matching(self, request, lang: str, word_length: int):
        request_serializer = RequestV1Serializer(data=request.data)
        if not request_serializer.is_valid():
            log.error("Errors: {}".format(request_serializer.errors))

            return HttpResponseServerError("Request data not formatted correctly!")


        req = request_serializer.validated_data
        word_length = int(word_length)
        words = DictionaryLoader.load(lang, word_length)
        word, prime, other = words.match_word(req["match_mask"], req["excluded_letters"], req["known_letters"])
        log.info("Done matching.")

        word_data = {
            "word": word,
            "prime_words": prime,
            "other_words": other
        }
        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = WordsV1Serializer(data=word_data)
        if not serializer.is_valid():
            log.error("Errors: {}".format(serializer.errors))

            return HttpResponseServerError("Data not formatted correctly!")

        return JsonResponse(serializer.validated_data)
