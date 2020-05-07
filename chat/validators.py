import json

import fastjsonschema

from chat import settings


scheme_validate_create_msg = fastjsonschema.compile({
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
                'kind': {
                    'type': 'string',
                    'enum': (
                        'file',
                        'text',
                    )
                },
                'text': {
                    'type': 'string',
                },
                'fileId': {
                    'type': 'number',
                }
            },
            'required': ('kind', ),
            'if': {
                'properties': {'kind': {'const': 'file'}},
            },
            'then': {
                'required': ('fileId', ),
            },
            'else': {
                'required': ('text', ),
            }

        },
    },
    'required': ('event', 'data'),
})

scheme_validate_user_typing = fastjsonschema.compile({
    'type': 'object',
    'properties': {
        'event': {
            'type': 'string',
            'enum': (
                settings.CHAT_USER_TYPING,
            ),
        },
    },
    'required': ('event', ),
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


validate_create_msg = make_validator(scheme_validate_create_msg)
validate_user_typing = make_validator(scheme_validate_user_typing)


def validate(data, validators=[validate_create_msg, validate_user_typing]):
    for validator in validators:
        validate_data = validator(data)
        if validate_data:
            return validate_data

