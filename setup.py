from setuptools import setup

setup(
    name='aiohttp_chat',
    version='0.1',
    author='Timur Safin',
    author_email='timurtlt96@mail.ru',
    packages=['chat'],
    url='https://github.com/Safintim/aiohttp-chat',
    license='MIT',
    description='Aiohttp websocket chat',
    install_requires=[
        'aiohttp',
        'aiopg',
        'SQLAlchemy',
        'psycopg2-binary',
        'PyYAML',
        'fastjsonschema'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Aiohttp',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
        'Natural Language :: Russian',
    ]
)
