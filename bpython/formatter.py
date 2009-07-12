# The MIT License
#
# Copyright (c) 2008 Bob Farrell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# A simple formatter for bpython to work with Pygments.
# Pygments really kicks ass, it made it really easy to
# get the exact behaviour I wanted, thanks Pygments.:)

import curses
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Token, Whitespace, Literal, Punctuation

"""These format strings are pretty ugly.
\x01 represents a colour marker, which
    can be proceded by one or two of
    the following letters:
    k, r, g, y, b, m, c, w, d
    Which represent:
    blacK, Red, Green, Yellow, Blue, Magenta,
    Cyan, White, Default
    e.g. \x01y for yellow,
        \x01gb for green on blue background

\x02 represents the bold attribute

\x03 represents the start of the actual
    text that is output (in this case it's
    a %s for substitution)

\x04 represents the end of the string; this is
    necessary because the strings are all joined
    together at the end so the parser needs them
    as delimeters

"""

Parenthesis = Token.Punctuation.Parenthesis

theme_map = {
    Keyword: 'keyword',
    Name: 'name',
    Comment: 'comment',
    String: 'string',
    Literal: 'string',
    Literal.String: 'string',
    Error: 'error',
    Number: 'number',
    Token.Literal.Number.Float: 'number',
    Operator: 'operator',
    Operator.Word: 'operator',
    Punctuation: 'punctuation',
    Token: 'token',
    Whitespace: 'background',
    Parenthesis: 'punctuation',
    Parenthesis.UnderCursor: 'operator'
}


class BPythonFormatter(Formatter):
    """This is the custom formatter for bpython.
    Its format() method receives the tokensource
    and outfile params passed to it from the
    Pygments highlight() method and slops
    them into the appropriate format string
    as defined above, then writes to the outfile
    object the final formatted string.

    See the Pygments source for more info; it's pretty
    straightforward."""

    f_strings = {}

    def __init__(self, color_scheme, **options):
        if not self.f_strings:
            for k, v in theme_map.iteritems():
                self.f_strings[k] = '\x01%s' % (color_scheme[v],)
                if k is Parenthesis:
                    # FIXME: Find a way to make this the inverse of the current
                    # background colour
                    self.f_strings[k] += 'I'
        Formatter.__init__(self, **options)

    def format(self, tokensource, outfile):
        o = ''
        curses.curs_set(1)
        for token, text in tokensource:
            if text == '\n':
                continue

            if token in self.f_strings:
                o +=  "%s\x03%s\x04" % (self.f_strings[token], text )
            else:
                o += "%s\x03%s\x04" % (self.f_strings[Token], text )
        outfile.write(o.rstrip())

# vim: sw=4 ts=4 sts=4 ai et
