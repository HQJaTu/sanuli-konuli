from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .wordv1serializer import WordV1Serializer

@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[]
)
class WordsV1Serializer(serializers.Serializer):
    found_matches = serializers.BooleanField(allow_null=False)
    word = serializers.CharField(max_length=10, allow_null=False, allow_blank=True)
    prime_words = serializers.ListSerializer(
        child=serializers.CharField(max_length=10, allow_null=False, allow_blank=False)
    )
    other_words = serializers.ListSerializer(
        child=serializers.CharField(max_length=10, allow_null=False, allow_blank=False)
    )
