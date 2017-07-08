from pccListener import pccListener


class pccPrintListener(pccListener):
    def __init__(self, name):
        super(pccPrintListener, self).__init__()
        self.code = "" # bytecode
        self.name = name


    def getBytecode(self):
        return self.code


    def enterProgram(self, ctx):
        self.code += '.class public %s' % self.name + '\n'
        self.code += '.super java/lang/Object' + '\n'

        self.code += '.method public <init>()V' + '\n'
        self.code += 'aload_0' + '\n'
        self.code += 'invokenonvirtual java/lang/Object/<init>()V' + '\n'
        self.code += 'return' + '\n'
        self.code += '.end method' + '\n'

        self.code += '.method public static main([Ljava/lang/String;)V' + '\n'
        self.code += '.limit stack 10000' + '\n' # hardcoded!


    def exitProgram(self, ctx):
        self.code += "return" + '\n'
        self.code += ".end method" + '\n'
