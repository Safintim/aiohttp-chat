from chat.db import chat, message, message_status, participant_chat


async def get_chat(conn, chat_id):
    chat_records = await conn.execute(
        chat.select().
        where(chat.c.id == chat_id),
    )
    return await chat_records.fetchone()


async def get_chat_participants(conn, chat_id):
    participant_records = await conn.execute(
        participant_chat.select().
        where(participant_chat.c.chat_id == chat_id),
    )
    return await participant_records.fetchall()


async def create_message(conn, chat_id, user_id, text):
    msg_records = await conn.execute(
        message.insert().
        returning(*message.c).
        values(chat_id=chat_id, user_id=user_id, text=text),
    )
    return await msg_records.fetchone()


async def bulk_create_message_statuses(conn, msg_id, user_ids):
    for user_id in user_ids:
        await conn.execute(
            message_status.insert().
            values(user_id),
        )


async def is_user_chat_participant(conn, _chat, _user):
    participant_records = await conn.execute(
        participant_chat.select().
        where(participant_chat.c.chat_id == _chat.id).
        where(participant_chat.c.user_id == _user.id),
    )
    participants = await participant_records.fetchall()
    participant_user_ids = [participant.user_id for participant in participants]

    return _user.id in participant_user_ids
