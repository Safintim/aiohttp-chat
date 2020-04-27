from chat.views import handle_chat, index_greet


def setup_routes(app):
    app.router.add_get('/ws/hi/', index_greet)
    app.router.add_get('/ws/chats/{chat_id}', handle_chat)
