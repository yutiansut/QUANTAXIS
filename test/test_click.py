#coding=utf-8

import click


@click.option(
    '-a',
    '--after',
    help='Clear all data after TIMESTAMP'
    ' This may not be passed with -k / --keep-last',
)
def prin():
    print('xxxx')