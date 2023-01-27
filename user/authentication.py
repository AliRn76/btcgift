import time
from datetime import timedelta

from jose import jwt, JOSEError

from .models import User
from .exceptions import AuthenticationException, UserBannedException
from config.settings import SECRET_KEY, JWT_EXP
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class JWTAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    algorithm = 'HS256'
    model = User

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 2:
            raise AuthenticationException

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationException

        return self.authenticate_credentials(token)

    @classmethod
    def authenticate_credentials(cls, token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[cls.algorithm])
        except JOSEError:
            raise AuthenticationException

        try:
            user = cls.model.objects.get(id=decoded_token['user_id'])
        except cls.model.DoesNotExist:
            raise AuthenticationException

        if user.is_banned:
            raise UserBannedException

        return user, token

    @staticmethod
    def encode_jwt_token(user: User):
        payload = {'user_id': user.id}
        access_exp = {'exp': time.time() + JWT_EXP}
        refresh_exp = {'exp': time.time() + JWT_EXP + timedelta(days=7).total_seconds()}
        tokens = {
            'access_token': jwt.encode(payload | access_exp, SECRET_KEY, JWTAuthentication.algorithm),
            'refresh_token': jwt.encode(payload | refresh_exp, SECRET_KEY, JWTAuthentication.algorithm),
        }
        return tokens

    def authenticate_header(self, request):
        return self.keyword
