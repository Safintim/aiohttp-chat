import os
import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'app.yaml'


def get_config(path):
    with open(path) as yamlfile:
        return yaml.safe_load(yamlfile)


config = get_config(config_path)

WS_CHAT_TIMEOUT = int(os.getenv('WS_CHAT_TIMEOUT', 10))
HEARTBEAT_TIMEOUT = os.getenv('HEARTBEAT_TIMEOUT')

if HEARTBEAT_TIMEOUT:
    HEARTBEAT_TIMEOUT = int(HEARTBEAT_TIMEOUT)


# events
CHAT_NEW_MESSAGE = 'CHAT_NEW_MESSAGE'
CHAT_CREATE_MESSAGE = 'CHAT_CREATE_MESSAGE'


USER_TABLE = os.getenv('USER_TABLE', 'app_user')

ENABLE_NOTIFICATION = os.getenv('ENABLE_NOTIFICATION', 'true').lower() in {'yes', '1', 'true'}
NOTIFICATION_TOKEN = os.getenv('NOTIFICATION_TOKEN', 'token')
NOTIFICATION_URL = os.getenv('NOTIFICATION_URL', 'http://0.0.0.0:8003/notification/')
