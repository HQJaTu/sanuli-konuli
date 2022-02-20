from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[]
)
class RequestV1Serializer(serializers.Serializer):
    match_mask = serializers.CharField(max_length=10, allow_null=False)
    excluded_letters = serializers.CharField(max_length=10, allow_null=False)
    known_letters = serializers.CharField(max_length=10, allow_null=False)
