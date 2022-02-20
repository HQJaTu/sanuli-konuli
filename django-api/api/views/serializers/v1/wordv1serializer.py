from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[]
)
class WordV1Serializer(serializers.Serializer):
    word = serializers.CharField(max_length=10, allow_null=False)
