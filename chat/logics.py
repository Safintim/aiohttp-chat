from chat import (
    events,
    messages,
    notifications,
    serializers,
    services,
    settings,
)


async def send_message(conn, ws_current, wss, chat, user, msg_data):
    if msg_data['kind'] == 'file':
        if await services.can_use_file(conn, msg_data['fileId']):
            await ws_current.send_json(
                {
                    'code': 1001,
                    'file': 'not exists or already taken',
                }
            )
            return

        message = await events.handle_msg_create(
            conn, chat, user, kind='file', file_id=msg_data['fileId'],
        )
    else:
        message = await events.handle_msg_create(
            conn, chat, user, kind='text', text=msg_data['text'],
        )

    message_data = await serializers.serialize_chat_message(conn, message)
    await messages.send_chat_message(
        wss, chatId=chat.id, **message_data,
    )
    participants = await services.get_chat_participants(
        conn, chat.id,
    )
    participant_ids = [
        participant.user_id
        for participant in participants
    ]

    if settings.ENABLE_NOTIFICATION:
        await notifications.push_message(
            participant_ids,
            chatId=chat.id,
            **message_data,
        )


async def user_typing(wss, ws_current, user):
    user_data = serializers.serialize_user(user)
    await messages.send_user_typing(
        wss, exclude=[ws_current], **user_data,
    )
