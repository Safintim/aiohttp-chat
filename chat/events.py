from chat import services, settings


def is_creation_msg_event(event):
    return event == settings.CHAT_CREATE_MESSAGE


async def handle_msg_create(conn, chat, user, text):
    msg = await services.create_message(conn, chat.id, user.id, text)
    chat_participants = await services.get_chat_participants(conn, chat.id)
    participant_ids = [
        {
            'user_id': participant.user_id,
            'message_id': msg.id,
            'is_read': participant.user_id == user.id,
        }
        for participant in chat_participants
    ]
    await services.bulk_create_message_statuses(conn, msg.id, participant_ids)
    return msg
