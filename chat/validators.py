import json

import fastjsonschema

from chat import settings


scheme_chat_msg = fastjsonschema.compile({
    'type': 'object',
    'properties': {
        'event': {
            'type': 'string',
            'enum': (
                settings.CHAT_CREATE_MESSAGE,
            ),
        },
        'data': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                },
            },
            'required': ('text', ),
        },
    },
    'required': ('event', 'data'),
})


def make_validator(validator):
    def inner(msg):  # noqa WPS430
        try:
            msg = validator(json.loads(msg))
        except (
            json.decoder.JSONDecodeError,
            fastjsonschema.JsonSchemaException,
        ):
            msg = None
        return msg
    return inner


chat_msg = make_validator(scheme_chat_msg)
