from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import permissions
from django.http import HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from ..authentication.token_authentication import TokenAuthentication
from .v1.words import API as APIv1
from .serializers.v1 import WordV1Serializer, WordsV1Serializer, RequestV1Serializer


class API(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = [
        "get", "post"
    ]
    schema = AutoSchema()

    @extend_schema(
        responses={
            200: WordV1Serializer,
            401: OpenApiTypes.STR,
            500: OpenApiTypes.STR,
        },
        parameters=[
            OpenApiParameter(
                name="lang",
                type=str,
                location=OpenApiParameter.PATH,
                description="Language for a pre-configured dictionary to use",
            ),
            OpenApiParameter(
                name="word_length",
                type=int,
                location=OpenApiParameter.PATH,
                description="Word length in dictionary",
            ),
            OpenApiParameter(
                name="excluded",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Letters to exclude",
            ),
        ],
        # override default docstring extraction
        description="Get initial word",
        # provide Authentication class that deviates from the views default
        # auth=None,
        # change the auto-generated operation name
        # operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
        # attach request/response examples to the operation.
    )
    def get(self, request, *args, **kwargs):
        if not request.version:
            return HttpResponseBadRequest("Need version!")

        version = int(request.version)
        if "version" in kwargs:
            # Note: It's pretty sure the value is there, but let's have an if just to be sure.
            del kwargs["version"]
        if version == 1:
            api = APIv1(request=request)
            return api.get_initial(request, *args, **kwargs)

        raise ValueError("Unknown version!")

    @extend_schema(
        request=RequestV1Serializer,
        responses={
            200: WordsV1Serializer,
            401: OpenApiTypes.STR,
            500: OpenApiTypes.STR,
        },
        parameters=[
            OpenApiParameter(
                name="lang",
                type=str,
                location=OpenApiParameter.PATH,
                description="Language for a pre-configured dictionary to use",
            ),
            OpenApiParameter(
                name="word_length",
                type=int,
                location=OpenApiParameter.PATH,
                description="Word length in dictionary",
            ),
        ],
        # override default docstring extraction
        description="Find matching word",
        # provide Authentication class that deviates from the views default
        # auth=None,
        # change the auto-generated operation name
        # operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
        # attach request/response examples to the operation.
    )
    def post(self, request, *args, **kwargs):
        if not request.version:
            return HttpResponseBadRequest("Need version!")

        version = int(request.version)
        if "version" in kwargs:
            # Note: It's pretty sure the value is there, but let's have an if just to be sure.
            del kwargs["version"]
        if version == 1:
            api = APIv1(request=request)
            return api.post_find_matching(request, *args, **kwargs)

        raise ValueError("Unknown version!")
