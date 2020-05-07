from chat import services, settings


def serialize_chat_message(conn, msg):
    relative_path = services.get_file(conn, msg.file_id)
    file_url = f'{settings.HOST}{relative_path}'
    return {
        'id': msg.id,
        'kind': msg.kind,
        'text': msg.text,
        'fileUrl': file_url,
        'createdAt': msg.created_at.isoformat(),
        'user': msg.user_id,
    }
