#coding:utf-8
from docopt import docopt


doc='Usage: my_program.py [-hso FILE] [--quiet | --verbose] [INPUT ...] \
\
-h --help    show this\
-s --sorted  sorted output\
-o FILE      specify output file [default: ./test.txt]\
--quiet      print less text\
--verbose    print more text'
docopt(doc, argv=None, help=True, version=None, options_first=False)