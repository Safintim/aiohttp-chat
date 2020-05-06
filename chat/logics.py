from chat import (
    events,
    messages,
    notifications,
    serializers,
    services,
    settings,
)


async def send_message(conn, wss, chat, user, text):
    message = await events.handle_msg_create(conn, chat, user, text)
    message_data = serializers.serialize_chat_message(message)
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
