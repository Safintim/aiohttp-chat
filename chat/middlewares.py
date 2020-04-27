import re

from aiohttp import web

from chat import services


def is_exclude(request, exclude):
    for pattern in exclude:
        if re.fullmatch(pattern, request.path):
            return True
    return False


def setup_middlewares(app):
    middlewares = [
        token_auth_middleware(exclude_routes=('/ws/hi/', )),
        chat_auth_middleware(exclude_routes=('/ws/hi/', r'/ws/fights/\d*')),
    ]
    app.middlewares.extend(middlewares)


def token_auth_middleware(
    request_property='user',
    auth_scheme='Token',
    exclude_routes=(),
    exclude_methods=(),
):

    @web.middleware  # noqa WPS430
    async def middleware(request, handler):  # noqa WPS110
        if is_exclude(request, exclude_routes) or request.method in exclude_methods:
            return await handler(request)

        try:
            scheme, token = request.headers['Authorization'].strip().split(' ')
        except KeyError:
            raise web.HTTPUnauthorized(reason='Missing authorization header')
        except ValueError:
            raise web.HTTPForbidden(reason='Invalid authorization header')
        if auth_scheme.lower() != scheme.lower():
            raise web.HTTPForbidden(reason='Invalid token scheme')

        async with request.app['db'].acquire() as conn:
            user = await services.get_user_id_by_token(conn, token)

        if user:
            request[request_property] = user
        else:
            raise web.HTTPForbidden(reason='Token doesnt exist')

        return await handler(request)

    return middleware


def chat_auth_middleware(
    identifier='chat_id',
    exclude_routes=(),
    exclude_methods=(),
):

    @web.middleware # noqa WPS430
    async def middleware(request, handler): # noqa WPS110
        if is_exclude(request, exclude_routes) or request.method in exclude_methods:
            return await handler(request)

        ident = request.match_info.get(identifier)

        if not ident:
            raise web.HTTPForbidden(reason='Missing identifier')

        async with request.app['db'].acquire() as conn:
            chat = await services.get_chat(conn, ident)

            if not chat:
                raise web.HTTPFound(
                    location='/hi',
                    reason='Not found chat with identifier',
                )

            if await services.is_user_chat_participant(conn, chat, request['user']):
                request['chat'] = chat
            else:
                raise web.HTTPForbidden(reason='Not auth for identifier')

            return await handler(request)

    return middleware
