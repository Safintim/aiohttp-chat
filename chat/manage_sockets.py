import logging

logger = logging.getLogger(__file__)


async def add_ws_to_channel(ws, channel_name, channels):
    if channels.get(channel_name):
        user_socket = list(filter(
            lambda ws_current: ws.user.id == ws_current.user.id,
            channels[channel_name],
        ))
        if user_socket:
            try:
                await user_socket[0].close()
            except Exception as e:
                logger.error(f'cleaadd_ws_to_channeln_channel {e}')
            channels[channel_name].discard(user_socket[0])
        channels[channel_name].add(ws)
    else:
        channels[channel_name] = {ws}


def delete_ws_from_channel(ws, channel_name, channels):
    channels[channel_name].discard(ws)
    if not channels[channel_name]:
        channels.pop(channel_name, None)
