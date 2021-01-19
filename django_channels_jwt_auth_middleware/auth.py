import traceback
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
from jwt import InvalidSignatureError, ExpiredSignatureError, DecodeError

from .settings import SIGNING_KEY


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            if(jwt_token_list := parse_qs(scope["query_string"].decode("utf8")).get('token', None)):
                jwt_token = jwt_token_list[0]
                user_info_from_jwt = jwt_decode(
                    jwt_token, SIGNING_KEY, algorithms=["HS256"])
                user_id = user_info_from_jwt['user_id']
                user = await self.get_logged_in_user(user_id)
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()
        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            traceback.print_exc()
        except:
            scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_logged_in_user(self, user_id):
        user = get_user_model().objects.get(id=user_id)
        return user


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
