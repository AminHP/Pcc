#! /usr/bin/env python

import sys
import os
import subprocess
from copy import deepcopy
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build'))

from antlr4 import *
from pccLexer import pccLexer
from pccParser import pccParser
from print_listener import pccPrintListener
from error_listener import pccLexerErrorListener, pccParserErrorListener, SyntaxErrorException
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
    return parser


def get_bytecode(parser, name):
    tree = parser.program()
    printer = pccPrintListener(name)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    return printer.getBytecode()


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


def create_class_file(bytecode, name, classes):
    if not os.path.exists('output'):
        os.mkdir('output')

    all_classes = classes.items() + [(name, bytecode)]

    for class_name, class_bytecode in all_classes:
        bcfile = os.path.join('output', class_name + '.bc')
        with open(bcfile, 'w') as f:
            f.write(class_bytecode)

        p = subprocess.Popen(['java', '-jar', 'bin/jasmin.jar', '-d', 'output', bcfile], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = p.communicate()
        if p[0]:
            print p[0]
        if p[1]:
            print p[1]



def run(code, name):
    # analyze
    lexer, stream = lex(load_code(code))
    tokens, lexical_errors = get_tokens(lexer)
    parser = parse(stream)
    parsing_errors = get_rules(parser)

    # generate code
    lexer, stream = lex(load_code(code))
    tokens, lexical_errors = get_tokens(lexer)
    parser = parse(stream)

    convert_error = ''
    try:
        bytecode, classes = get_bytecode(parser, name)
        if not lexical_errors and not parsing_errors:
            create_class_file(bytecode, name, classes)
    except Exception as e:
        convert_error = e

    return tokens, lexical_errors, parsing_errors, convert_error



if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        run(f.read(), sys.argv[2])
