from chat import db


async def get_chat(conn, chat_id):
    chat_records = await conn.execute(
        db.chat.select().
        where(db.chat.c.id == chat_id),
    )
    return await chat_records.fetchone()


async def get_chat_participants(conn, chat_id):
    participant_records = await conn.execute(
        db.participant_chat.select().
        where(db.participant_chat.c.chat_id == chat_id),
    )
    return await participant_records.fetchall()


async def get_users(conn):
    user_records = await conn.execute(db.user.select())
    return await user_records.fetchall()


async def get_tokens(conn):
    token_records = await conn.execute(db.token.select())
    return await token_records.fetchall()


async def get_user_id_by_token(conn, user_token):
    token_records = await conn.execute(
        db.token.select().
        where(db.token.c.key == user_token),
    )

    token_record = await token_records.fetchone()

    if not token_record:
        return None

    user_records = await conn.execute(
        db.user.select().
        where(db.user.c.id == token_record.user_id),
    )
    return await user_records.fetchone()


async def create_message(conn, chat_id, user_id, text):
    msg_records = await conn.execute(
        db.message.insert().
        returning(*db.message.c).
        values(chat_id=chat_id, user_id=user_id, text=text),
    )
    return await msg_records.fetchone()


async def bulk_create_message_statuses(conn, msg_id, user_ids):
    for user_id in user_ids:
        await conn.execute(
            db.message_status.insert().
            values(user_id),
        )


async def is_user_chat_participant(conn, _chat, _user):
    participant_records = await conn.execute(
        db.participant_chat.select().
        where(db.participant_chat.c.chat_id == _chat.id).
        where(db.participant_chat.c.user_id == _user.id),
    )
    participants = await participant_records.fetchall()
    participant_user_ids = [participant.user_id for participant in participants]

    return _user.id in participant_user_ids
