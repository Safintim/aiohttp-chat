from chat import services, settings


async def serialize_chat_message(conn, msg):
    media = await services.get_file(conn, msg.file_id)
    file_url = f'{settings.HOST}{media.file}'
    is_me_readed = True  # because its my msg
    # TODO need test is_someone_read_message
    is_someone_readed = await services.is_someone_read_message(conn, msg)
    return {
        'id': msg.id,
        'kind': msg.kind,
        'text': msg.text,
        'fileUrl': file_url,
        'isMeReaded': is_me_readed,
        'isSomeoneReaded': is_someone_readed,
        'createdAt': msg.created_at.isoformat(),
        'user': msg.user_id,
    }
