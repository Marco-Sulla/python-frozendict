from distutils.core import setup

setup(
    name     = 'frozendict',
    version  = '0.1',

    author       = 'Santiago Lezica',
    author_email = 'slezica89@gmail.com',

    packages = ['frozendict'],
    license  = 'MIT License',

    description      = 'An immutable dictionary',
    long_description = open('README.txt').read()
)
