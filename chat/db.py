import datetime

from aiopg import sa
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Sequence,
    String,
    Table,
    Text,
)

from chat.settings import USER_TABLE


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


meta = MetaData()

user = Table(
    USER_TABLE,
    meta,
    Column('id', Integer, primary_key=True),
)

token = Table(
    'authtoken_token',
    meta,
    Column('key', String(40), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
)

chat = Table(
    'chat_chat',
    meta,
    Column('id', Integer, primary_key=True),
)

participant_chat = Table(
    'chat_participantchat',
    meta,
    Column('id', Integer, primary_key=True),
    Column('chat_id', Integer, ForeignKey('chat.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
)

message = Table(
    'chat_message',
    meta,
    Column('id', Integer, Sequence('app_message_id_seq'), primary_key=True),
    Column('text', Text),
    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('chat_id', Integer, ForeignKey('chat.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
)

message_status = Table(
    'chat_messagestatus',
    meta,
    Column(
        'id', Integer, Sequence('app_messagestatus_id_seq'), primary_key=True,
    ),
    Column('is_read', Boolean, default=False),
    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('message_id', Integer, ForeignKey('message.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('user.id', ondelete='CASCADE')),
)
