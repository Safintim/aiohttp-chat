import os
import pathlib


BASE_DIR = pathlib.Path(__file__).parent

config = {
    'postgres': {
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }
}


WS_CHAT_TIMEOUT = int(os.getenv('WS_CHAT_TIMEOUT', 10))
HEARTBEAT_TIMEOUT = os.getenv('HEARTBEAT_TIMEOUT')

if HEARTBEAT_TIMEOUT:
    HEARTBEAT_TIMEOUT = int(HEARTBEAT_TIMEOUT)


# events
CHAT_NEW_MESSAGE = 'CHAT_NEW_MESSAGE'
CHAT_CREATE_MESSAGE = 'CHAT_CREATE_MESSAGE'
CHAT_USER_TYPING = 'CHAT_USER_TYPING'


USER_TABLE = os.getenv('USER_TABLE', 'app_user')

ENABLE_NOTIFICATION = os.getenv('ENABLE_NOTIFICATION', 'false').lower() in {'yes', '1', 'true'}
NOTIFICATION_TOKEN = os.getenv('NOTIFICATION_TOKEN', 'token')
NOTIFICATION_URL = os.getenv('NOTIFICATION_URL', 'http://0.0.0.0:8003/notification/')

HEADER_AUTH = os.getenv('HEADER_AUTH', 'false').lower() in {'yes', '1', 'true'}
HOST = os.getenv('HOST', 'http://127.0.0.1:8000/')
