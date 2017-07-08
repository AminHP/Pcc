from pccListener import pccListener


class pccPrintListener(pccListener):
    def __init__(self, name):
        super(pccPrintListener, self).__init__()
        self.code = "" # bytecode
        self.name = name


    def getBytecode(self):
        return self.code


    def _add_ins(self, instruction):
        self.code += instruction + '\n'


    def enterProgram(self, ctx):
        self._add_ins('.class public %s' % self.name)
        self._add_ins('.super java/lang/Object')

        self._add_ins('.method public <init>()V')
        self._add_ins('aload_0')
        self._add_ins('invokenonvirtual java/lang/Object/<init>()V')
        self._add_ins('return')
        self._add_ins('.end method')

        self._add_ins('.method public static main([Ljava/lang/String;)V')
        self._add_ins('.limit stack 10000') # hardcoded!


    def exitProgram(self, ctx):
        self._add_ins("return")
        self._add_ins(".end method")
