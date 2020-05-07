import json

from chat import validators
from chat.settings import CHAT_CREATE_MESSAGE, CHAT_USER_TYPING


def test_validate_chat_msg_file():
    body = {
        'event': CHAT_CREATE_MESSAGE,
        'data': {
            'kind': 'file',
            'fileId': 1,
        }
    }

    json_data = json.dumps(body)
    assert validators.validate(json_data)


def test_validate_chat_msg_text():
    body = {
        'event': CHAT_CREATE_MESSAGE,
        'data': {
            'kind': 'text',
            'text': 'Hello',
        }
    }

    json_data = json.dumps(body)
    assert validators.validate(json_data)


def test_validate_chat_msg_without_required():
    body = {
        'event': CHAT_CREATE_MESSAGE,
        'data': {
            'kind': 'text',
        }
    }

    json_data = json.dumps(body)
    assert not validators.validate(json_data)

    body['data']['kind'] = 'file'
    json_data = json.dumps(body)
    assert not validators.validate(json_data)

    body['data']['text'] = 'hello'
    json_data = json.dumps(body)
    assert not validators.validate(json_data)

    body['data']['kind'] = 'text'
    body['data']['fileId'] = 1
    body['data'].pop('text')
    json_data = json.dumps(body)
    assert not validators.validate(json_data)

    body = {
        'event': CHAT_CREATE_MESSAGE
    }
    json_data = json.dumps(body)
    assert not validators.validate(json_data)


def test_validate_user_typing():
    body = {
        'event': CHAT_USER_TYPING,
    }
    json_data = json.dumps(body)
    assert validators.validate(json_data)
