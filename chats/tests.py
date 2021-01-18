import json
import pytest
from channels.generic.websocket import WebsocketConsumer
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import path
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode

from middleware.jwt_auth_middleware import JWTAuthMiddlewareStack


class TesterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data, bytes_data):
        user = self.scope['user']
        self.send(text_data=json.dumps({'user': user}))

    def disconnect(self, code):
        self.disconnect()


class WebsocketTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="example user", email='', password="Abcd1234")
        self.jwt = jwt_encode({'user_id': self.user.id},
                              settings.SECRET_KEY, algorithm='HS256')

    async def test_connection_with_token(self):
        app = JWTAuthMiddlewareStack(URLRouter([
            path('ws/chat/<str:room_name>/', TesterConsumer.as_asgi()),
        ]))
        communicator = WebsocketCommunicator(
            app, f'ws/chat/example/?token={self.jwt}')
        connect, subprotocol = await communicator.connect()
        assert connect
        response = await communicator.receive_from()
        # assert response['user'] == 1
        await communicator.disconnect()


# @pytest.mark.django_db
# @pytest.mark.asyncio
# async def test_connection_with_token():
#     # setup
#     user = get_user_model().objects.create_user(
#         username="example user", email='', password="Abcd1234")
#     user_info = {'user_id': user.id}
#     encoded_jwt = jwt_encode(user_info, settings.SECRET_KEY, algorithm='HS256')
#     # set authentication stack
#     app = JWTAuthMiddlewareStack(TesterConsumer.as_asgi())
#     communicator = WebsocketCommunicator(
#         app, f'ws/chat/example/?token={encoded_jwt}')
#     connect, subprotocol = await communicator.connect()
#     assert connect
#     response = await communicator.receive_from()
#     assert response['user'] == 1
#     await communicator.disconnect()
