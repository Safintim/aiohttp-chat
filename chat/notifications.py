import logging

import aiohttp

from chat import settings

logger = logging.getLogger(__name__)


async def send_notification(payload):
    headers = {'Authorization': f'token {settings.NOTIFICATION_TOKEN}'}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            resp = await session.post(settings.NOTIFICATION_URL, json=payload)
            data = await resp.json()
            logger.info(f'send_notification {data}')
    except aiohttp.ClientError as error:
        logger.error(f'send_notification {error}')


async def push_message(user_ids, **kwargs):
    title = 'Сообщение'
    body = 'У вас новое сообщение'
    kwargs['typeEvent'] = settings.CHAT_NEW_MESSAGE
    payload = {
        'title': title,
        'body': body,
        'user_ids': user_ids,
        'typeEvent': settings.CHAT_NEW_MESSAGE,
        **kwargs,
    }
    await send_notification(payload)
