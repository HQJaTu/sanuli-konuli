from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .wordv1serializer import WordV1Serializer

@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[]
)
class WordsV1Serializer(serializers.Serializer):
    word = serializers.CharField(max_length=10, allow_null=False)
    prime_words = serializers.ListSerializer(child=serializers.CharField(max_length=10, allow_null=False))
    other_words = serializers.ListSerializer(child=serializers.CharField(max_length=10, allow_null=False))
