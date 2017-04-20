#! /usr/bin/env python

import sys
import os
from copy import deepcopy
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))

from antlr4 import *
from pccLexer import pccLexer
from pccParser import pccParser
from listener import pccPrintListener, pccLexerErrorListener, pccParserErrorListener, SyntaxErrorException
from antlr4.error.ErrorListener import ErrorListener


def load_code(code):
    return InputStream(code)


def lex(code):
    lexer = pccLexer(code)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    return lexer, stream


def parse(stream):
    parser = pccParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(pccParserErrorListener());
    #tree = parser.program()
    #printer = pccPrintListener()
    #walker = ParseTreeWalker()
    #walker.walk(printer, tree)
    return parser


def get_tokens(lexer):
    l = deepcopy(lexer)
    l.addErrorListener(pccLexerErrorListener());
    all_tokens = []
    all_errors = []

    while True:
        try:
            next_token = l.nextToken()
            if next_token.type == next_token.EOF:
                break
            all_tokens.append((l.symbolicNames[next_token.type], next_token))
        except SyntaxErrorException as e:
            all_errors.append(e)
            l.recover(e)

    return all_tokens, all_errors


def get_rules(parser):
    all_errors = []
    parser.program()
    all_errors = parser._listeners[-1].errors
    return all_errors



def run(code):
    lexer, stream = lex(load_code(code))
    tokens, lexical_errors = get_tokens(lexer)
    parser = parse(stream)
    parsing_errors = get_rules(parser)
    return tokens, lexical_errors, parsing_errors



if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        run(f.read())
