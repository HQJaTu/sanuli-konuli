from rest_framework.authentication import (
    TokenAuthentication as Django_TokenAuthentication,
)
from ..models.token_auth import Token


class TokenAuthentication(Django_TokenAuthentication):
    model = Token