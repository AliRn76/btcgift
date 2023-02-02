from rest_framework import status
from rest_framework.exceptions import APIException

from config.messages import *


class AuthenticationException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = AuthenticationMessage


class UserBannedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = UserBannedMessage
