import json

from channels.generic.websocket import WebsocketConsumer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import path
from jwt import encode as jwt_encode

from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack


User = get_user_model()


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    # def disconnect(self, code):
    #     self.disconnect()

    def receive(self, text_data, bytes_data=None):
        context = {
            'message': 'testing consumer',
        }
        user = self.scope['user']
        if (user_id := user.id):
            context.update({'user': str(user_id)})
        else:
            context.update({'user': None})
        self.send(text_data=json.dumps(context))


class JWTAuthMiddlewareTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='example', email='example@example.com', password='Abcd1234')
        self.jwt_token = jwt_encode(
            {'user_id': str(self.user.id)}, settings.SECRET_KEY, algorithm='HS256')

    async def test_middleware_without_token(self):
        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:room_name>/', TestConsumer.as_asgi()),
            ])
        )
        test_url = f'ws/chat/lobby/'
        communicator = WebsocketCommunicator(application, test_url)
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.send_to(text_data=json.dumps({'message': 'test'}))
        response = await communicator.receive_from()
        decoded_response = json.loads(response)
        self.assertIsNone(decoded_response['user'])
        await communicator.disconnect()

    async def test_middleware_with_token_query_string_but_no_value(self):
        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:room_name>/', TestConsumer.as_asgi()),
            ])
        )
        test_url = f'ws/chat/lobby/?token='
        communicator = WebsocketCommunicator(application, test_url)
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.send_to(text_data=json.dumps({'message': 'test'}))
        response = await communicator.receive_from()
        decoded_response = json.loads(response)
        self.assertIsNone(decoded_response['user'])
        await communicator.disconnect()
