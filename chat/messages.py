import logging

from chat import settings

logger = logging.getLogger(__file__)


async def send_chat_message(wss, exclude=None, **kwargs):
    message = {
        'event': settings.CHAT_NEW_MESSAGE,
        'data': kwargs,
    }
    await send_message_for_channel(message, wss, exclude)


async def send_user_typing(wss, exclude=None, **kwargs):
    message = {
        'event': settings.CHAT_USER_TYPING,
        'data': kwargs,
    }
    await send_message_for_channel(message, wss, exclude)


async def send_message_for_channel(message, wss, exclude=None):
    if not exclude:
        exclude = []
    for ws in filter(lambda _ws: _ws not in exclude, wss):
        try:
            await ws.send_json(message)
        except Exception as e:
            logger.error(f'send_message_for_channel {e}')
