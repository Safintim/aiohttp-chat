
def serialize_chat_message(msg):
    return {
        'id': msg.id,
        'text': msg.text,
        'createdAt': msg.created_at.isoformat(),
        'user': msg.user_id,
    }
