import logging

import aiohttp
from aiohttp import web

from chat import events, logics, settings, validators
from chat.manage_sockets import add_ws_to_channel, delete_ws_from_channel

logger = logging.getLogger(__file__)


async def index_greet(request):
    return web.json_response({'data': 'Hello, React Native'})


async def handle_chat(request):
    ws_current = web.WebSocketResponse(
        timeout=settings.WS_CHAT_TIMEOUT,
        heartbeat=settings.HEARTBEAT_TIMEOUT,
    )
    user = request['user']
    chat = request['chat']
    channel_name = f'channel-chat:{chat.id}'
    websockets_channels = request.app['websockets_channels']
    database = request.app['db']

    await ws_current.prepare(request)
    await ws_current.send_json({
        'event': 'connect',
        'code': 101,
        'message': f'hi user_{user.id}',
    })

    logger.debug(f'chat {chat.id}. user{user.id}. connect')
    logger.debug(f'websockets_channels {websockets_channels.get(channel_name)}')
    ws_current.user = user

    await add_ws_to_channel(ws_current, channel_name, websockets_channels)

    async with database.acquire() as conn:
        wss = websockets_channels[channel_name]
        async for msg in ws_current:
            logger.debug(f'chat {chat.id}. user {user.id}. {msg}')
            if msg.type != aiohttp.WSMsgType.TEXT:
                break
            msg_data = validators.validate(msg.data)
            if not msg_data:
                await ws_current.send_json({'code': 1001})
                continue
            if events.is_creation_msg_event(msg_data['event']):
                await logics.send_message(
                    conn=conn,
                    ws_current=ws_current,
                    wss=wss,
                    chat=chat,
                    user=user,
                    msg_data=msg_data['data'],
                )
            elif events.is_user_typing_event(msg_data['event']):
                await logics.user_typing(
                    wss=wss,
                    ws_current=ws_current,
                    user=user,
                )

    delete_ws_from_channel(ws_current, channel_name, websockets_channels)
    logger.debug(f'chat {chat.id}. user{user.id}. close')
    return ws_current
