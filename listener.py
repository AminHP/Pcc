from pccListener import pccListener
from antlr4.error.ErrorListener import ErrorListener


class pccPrintListener(pccListener):
    def enterInt_dec(self, ctx):
        #print "pcc: %s" % ctx.Id()
        pass


class pccErrorListener(ErrorListener):

    def __init__(self):
        super(pccErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxErrorException(line, column, msg)

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
