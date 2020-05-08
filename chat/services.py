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


async def get_file(conn, file_id):
    file_records = await conn.execute(
        db.media.select().
        where(db.media.c.id == file_id),
    )
    return await file_records.fetchone()


async def get_messages(conn, chat_id):
    message_records = await conn.execute(
        db.message.select().
        where(db.message.c.chat_id == chat_id),
    )
    return await message_records.fetchall()


async def get_message_by_file_id(conn, file_id):
    message_records = await conn.execute(
        db.message.select().
        where(db.message.c.file_id == file_id),
    )
    return await message_records.fetchone()


async def can_use_file(conn, file_id):
    is_exist_file = await get_file(conn, file_id)
    is_exist_message_with_file = await get_message_by_file_id(conn, file_id)
    return not is_exist_file or is_exist_message_with_file


async def create_message(conn, chat_id, user_id, kind, text=None, file_id=None):
    msg_records = await conn.execute(
        db.message.insert().
        returning(*db.message.c).
        values(
            chat_id=chat_id,
            user_id=user_id,
            kind=kind,
            text=text,
            file_id=file_id,
        ),
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


async def is_someone_read_message(conn, message):
    message_status_records = conn.execute(
        db.message_status.select().
        where(
            db.message_status.c.user_id != message.user_id,
            db.message_status.c.message_id == message.id,
            is_read == True,
        )
    )
    records = await message_status_records.fetchall()
    return bool(records)
