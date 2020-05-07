from chat import events, services, serializers
from chat.main import web_app


# for run test set database environment variables
# it's shit i know, but faster


async def test_hi(aiohttp_client):
    app = await web_app()
    client = await aiohttp_client(app)
    resp = await client.get('/ws/hi/')
    assert await resp.json() == {'data': 'Hello, React Native'}


async def test_chat_get_without_auth(aiohttp_client):
    app = await web_app()
    client = await aiohttp_client(app)
    resp = await client.get('/ws/chats/1')
    assert resp.status == 401


async def test_chat_connect(aiohttp_client):
    app = await web_app()
    client = await aiohttp_client(app)
    fake_token = '39300d281808ebb303f55e35a8b1e8d4ee2c179b'
    resp = await client.ws_connect(f'/ws/chats/1?token={fake_token}')
    expected = {'event': 'connect', 'code': 101, 'message': 'hi user_1'}
    assert await resp.receive_json() == expected


async def test_handle_msg_create(aiohttp_client):
    app = await web_app()
    await aiohttp_client(app)
    fake_token = '39300d281808ebb303f55e35a8b1e8d4ee2c179b'
    async with app['db'].acquire() as conn:
        chat = await services.get_chat(conn, 1)
        user = await services.get_user_id_by_token(conn, fake_token)
        assert await events.handle_msg_create(
            conn, chat, user, kind='text', text='TestMsg',
        )

        # it's work when exists file with id=1 and only one message
        # assert await events.handle_msg_create(
        #     conn, chat, user, kind='file', file_id=1,
        # )


async def test_serializer_msg(aiohttp_client):
    app = await web_app()
    await aiohttp_client(app)
    async with app['db'].acquire() as conn:
        message = await services.get_message_by_file_id(conn, file_id=1)
        serializer = await serializers.serialize_chat_message(conn, message)
        assert serializer['kind'] == 'file'