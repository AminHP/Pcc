from pccListener import pccListener
from error_listener import NotDeclaredException
from pccLexer import pccLexer


class pccPrintListener(pccListener):
    def __init__(self, name):
        super(pccPrintListener, self).__init__()
        self.code = "" # bytecode
        self.name = name
        self.block_number = 0
        self.variable_table = {}


    def newVar(self, name):
        new_id = len(self.variable_table) + 1 
        self.variable_table[(name, self.block_number)] = new_id
        return new_id


    def getVar(self, name, block):
        while True:
            if (name, block) in self.variable_table:
                break
            block = block - 1
            if block < 0:
                raise NotDeclaredException(name)
        return self.variable_table[(name, block)]


    def getBytecode(self):
        return self.code


    def _add_ins(self, instruction):
        self.code += instruction + '\n'



    def enterCompoundStatement(self, ctx):
        self.block_number +=1

    def exitCompoundStatement(self, ctx):
        self.block_number -=1


    def println(self, var_id, var_type, arr_index=None):
        if var_type == 'int':
            var_type = 'I'

        self._add_ins("getstatic java/lang/System/out Ljava/io/PrintStream;")

        if arr_index:
            self._add_ins('aload %s' % var_id)
            self._add_ins('bipush %s' % arr_index)
            self._add_ins('iaload')
        else:
            self._add_ins("iload %s" % var_id)

        self._add_ins("invokevirtual java/io/PrintStream/println(%s)V" % var_type)


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
        self._add_ins('.limit locals 10000') # hardcoded!


    def exitProgram(self, ctx):
        self._add_ins("return")
        self._add_ins(".end method")


    def enterDeclaration(self, ctx):
        vartype, ids, _ = list(ctx.getChildren())
        vartype = vartype.getText()

        for child in ids.getChildren():
            if child.getText() == ',':
                continue
            c = child.getChild(0)
            c = self.getLastChild(child)
            c_count = c.getChildCount()

            if c_count == 0 or c_count == 3: # var
                var_id = self.newVar((c.getChild(0) if c_count == 3 else c).getText()) # TODO: raise exception if variable exists
                if vartype == 'int':
                    self._add_ins("bipush 0")
                    self._add_ins("istore %s" % var_id)

            elif c_count == 4: # array
                var_id = self.newVar(c.getChild(0).getText()) # TODO: raise exception if variable exists
                size = c.getChild(2).getText()
                self._add_ins("bipush %s" % size)
                self._add_ins("newarray %s" % vartype)
                self._add_ins("astore %s" % var_id)

            if c_count == 3: # declration with assignment
                self.enterAssignmentExpression(c)


    def enterAssignmentExpression(self, ctx):
        if ctx.getChildCount() == 3:
            assignee, _, value = list(ctx.getChildren())
            assignee = self.getLastChild(assignee)
            if assignee.getChildCount() == 0: # identifier
                var_id = self.getVar(assignee.getText(), self.block_number)
                self.calculateExpression(value)
                self._add_ins("istore %s" % var_id)

            elif assignee.getChildCount() == 4: # array
                var_id = self.getVar(assignee.getChild(0).getText(), self.block_number)
                index = assignee.getChild(2)
                self._add_ins('aload %s' % var_id)
                self.calculateExpression(index)
                self.calculateExpression(value)
                self._add_ins('iastore')

            elif assignee.getChildCount() == 3: # struct
                pass


    def calculateExpression(self, ctx):
        ctx = self.getLastChild(ctx)

        if ctx.getChildCount() == 0: # identifier or constant value
            if ctx.getSymbol().type == pccLexer.Identifier:
                var_id = self.getVar(ctx.getText(), self.block_number)
                self._add_ins("iload %s" % var_id)
            else:
                self._add_ins("bipush %s" % ctx.getText())

        if ctx.getChildCount() == 4: # array value
            var_id = self.getVar(ctx.getChild(0).getText(), self.block_number)
            arr_index = ctx.getChild(2)
            self._add_ins('aload %s' % var_id)
            self.calculateExpression(arr_index)
            self._add_ins('iaload')

        elif ctx.getChildCount() == 3: # expr
            if ctx.getChild(0).getText() == '(':
                self.calculateExpression(ctx.getChild(1))
            else:
                i1, o, i2 = ctx.getChildren()
                o = o.getText()

                self.calculateExpression(i1)
                self.calculateExpression(i2)
                if o == '+':
                    self._add_ins("iadd")
                elif o == '-':
                    self._add_ins("isub")
                elif o == '*':
                    self._add_ins("imul")
                elif o == '/':
                    self._add_ins("idiv")



    def getLastChild(self, ctx):
        if ctx.getChildCount() == 0 or ctx.getChildCount() > 1:
            return ctx
        return self.getLastChild(ctx.getChild(0))
