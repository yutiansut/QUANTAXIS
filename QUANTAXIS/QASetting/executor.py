# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import print_function
from subprocess import Popen, PIPE, STDOUT

# Globals ######################################################################
DEBUG = False


def execute(command, shell=None, working_dir=".", echo=False, echo_indent=0):
    """Execute a command on the command-line.
    :param str,list command: The command to run
    :param bool shell: Whether or not to use the shell.  This is optional; if
        ``command`` is a basestring, shell will be set to True, otherwise it will
        be false.  You can override this behavior by setting this parameter
        directly.
    :param str working_dir: The directory in which to run the command.
    :param bool echo: Whether or not to print the output from the command to
        stdout.
    :param int echo_indent: Any number of spaces to indent the echo for clarity
    :returns: tuple: (return code, stdout)
    Example
        >>> from executor import execute
        >>> return_code, text = execute("dir")
    """
    if shell is None:
        shell = True if isinstance(command, str) else False

    p = Popen(command, stdin=PIPE, stdout=PIPE,
              stderr=STDOUT, shell=shell, cwd=working_dir)

    if echo:
        stdout = ""
        while p.poll() is None:
            # This blocks until it receives a newline.
            line = p.stdout.readline()
            print(" " * echo_indent, line, end="")
            stdout += line

        # Read any last bits
        line = p.stdout.read()
        print(" " * echo_indent, line, end="")
        print()
        stdout += line
    else:
        stdout, _ = p.communicate()

    return (p.returncode, stdout)
