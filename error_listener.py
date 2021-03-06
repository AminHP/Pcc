from antlr4.error.ErrorListener import ErrorListener


class pccLexerErrorListener(ErrorListener):

    def __init__(self):
        super(pccLexerErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxErrorException(line, column, msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("")


class pccParserErrorListener(ErrorListener):

    def __init__(self):
        super(pccParserErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(SyntaxErrorException(line, column, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception("")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception("")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception("")



class SyntaxErrorException(Exception):
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg
        self.error_msg = "%s:%s: %s" % (line, column, msg)
        super(SyntaxErrorException, self).__init__(self.error_msg)


class NotDeclaredException(Exception):
    def __init__(self, identifier):
        super(NotDeclaredException, self).__init__("'%s' not declared" % identifier)


class RedeclarationException(Exception):
    def __init__(self, identifier):
        super(RedeclarationException, self).__init__("'%s' previously declared" % identifier)
