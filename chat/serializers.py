from chat import services, settings


async def serialize_chat_message(conn, msg):
    media = await services.get_file(conn, msg.file_id)
    file_url = f'{settings.HOST}{media.file}'
    return {
        'id': msg.id,
        'kind': msg.kind,
        'text': msg.text,
        'fileUrl': file_url,
        'createdAt': msg.created_at.isoformat(),
        'user': msg.user_id,
    }
