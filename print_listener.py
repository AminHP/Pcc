from pccListener import pccListener
from error_listener import NotDeclaredException
from pccLexer import pccLexer
from pccParser import pccParser


class pccPrintListener(pccListener):
    def __init__(self, name):
        super(pccPrintListener, self).__init__()
        self.code = ""  # bytecode
        self.name = name
        self.block_number = 0
        self.label_number = 0
        self.variable_number = 1
        self.variable_table = {}
        self.var_type_table = {
            'int': 'i',
            'float': 'f',
            'double': 'd',
            'long': 'l',
            'char': 'i'
        }
        self.print_var_type_table = {
            'int': 'I',
            'float': 'F',
            'double': 'D',
            'long': 'J',
            'char': 'C'
        }
        self.constant_table = {
            'int': 'ldc',
            'float': 'ldc',
            'double': 'ldc2_w',
            'long': 'ldc2_w',
            'char': 'bipush'
        }

    def newVar(self, name, vtype):
        size = 2 if vtype in ('long', 'double') else 1
        self.variable_table[(name, self.block_number)] = (self.variable_number, vtype)
        self.variable_number += size
        return self.variable_number - size

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

    def _add_ins(self, instruction, var_type=None):
        v = self.var_type_table[var_type] if var_type else ''
        self.code += v + instruction + '\n'

    def _push_constant(self, constant, var_type):
        constant = str(constant)
        if var_type == 'float' or var_type == 'double':
            constant += '.' if not '.' in constant else ''
        elif var_type == 'char':
            constant = ord(constant.replace("'", ""))

        self._add_ins("%s %s" % (self.constant_table[var_type], constant))

    def enterCompoundStatement(self, ctx):
        self.block_number += 1
        if ctx.getChildCount() == 3:
            self.enterBlockItemList(ctx.getChild(1))

    def exitCompoundStatement(self, ctx):
        for name, block_number in self.variable_table.keys():
            if block_number == self.block_number:
                del self.variable_table[(name, block_number)]
        self.block_number -= 1

    def println(self, var_id, var_type, arr_index=None):
        self._add_ins("getstatic java/lang/System/out Ljava/io/PrintStream;")

        if arr_index:
            self._add_ins('aload %s' % var_id)
            self._add_ins('ldc %s' % arr_index)
            self._add_ins('aload', var_type)
        else:
            self._add_ins("load %s" % var_id, var_type)

        self._add_ins("invokevirtual java/io/PrintStream/println(%s)V" % self.print_var_type_table[var_type])

    def enterProgram(self, ctx):
        self._add_ins('.class public %s' % self.name)
        self._add_ins('.super java/lang/Object')

        self._add_ins('.method public <init>()V')
        self._add_ins('aload_0')
        self._add_ins('invokenonvirtual java/lang/Object/<init>()V')
        self._add_ins('return')
        self._add_ins('.end method')

        self._add_ins('.method public static main([Ljava/lang/String;)V')
        self._add_ins('.limit stack 10000')  # hardcoded!
        self._add_ins('.limit locals 10000')  # hardcoded!

    def exitProgram(self, ctx):
        self._add_ins("return")
        self._add_ins(".end method")

    def enterDeclaration(self, ctx):
        var_type, ids, _ = list(ctx.getChildren())
        var_type = var_type.getText()

        for child in ids.getChildren():
            if child.getText() == ',':
                continue
            c = child.getChild(0)
            c = self.getLastChild(child)
            c_count = c.getChildCount()

            if c_count == 0 or c_count == 3:  # var
                var_id = self.newVar((c.getChild(0) if c_count == 3 else c).getText(), var_type)  # TODO: raise exception if variable exists
                self._push_constant(0, var_type)
                self._add_ins("store %s" % var_id, var_type)

            elif c_count == 4: # array
                var_id = self.newVar(c.getChild(0).getText(), var_type) # TODO: raise exception if variable exists
                size = c.getChild(2).getText()
                self._add_ins("ldc %s" % size)
                self._add_ins("newarray %s" % var_type)
                self._add_ins("astore %s" % var_id)

            if c_count == 3:  # declration with assignment
                self.enterAssignmentExpression(c)

    def enterAssignmentExpression(self, ctx):
        if ctx.getChildCount() == 3:
            assignee, _, value = list(ctx.getChildren())
            assignee = self.getLastChild(assignee)
            if assignee.getChildCount() == 0:  # identifier
                var_id, var_type = self.getVar(assignee.getText(), self.block_number)
                self.calculateExpression(value, var_type)
                self._add_ins("store %s" % var_id, var_type)

            elif assignee.getChildCount() == 4:  # array
                var_id, var_type = self.getVar(assignee.getChild(0).getText(), self.block_number)
                index = assignee.getChild(2)
                self._add_ins('aload %s' % var_id)
                self.calculateExpression(index, 'int')
                self.calculateExpression(value, var_type)
                self._add_ins('astore', var_type)

            elif assignee.getChildCount() == 3:  # struct
                pass

    def calculateExpression(self, ctx, var_type):
        ctx = self.getLastChild(ctx)

        if ctx.getChildCount() == 0:  # identifier or constant value
            if ctx.getSymbol().type == pccLexer.Identifier:  # identifier
                var_id, vt = self.getVar(ctx.getText(), self.block_number)
                if vt != var_type:
                    raise TypeError("wrong type '%s'" % ctx.getText())
                self._add_ins("load %s" % var_id, var_type)
            else:  # constant value
                self._push_constant(ctx.getText(), var_type)

        if ctx.getChildCount() == 4:  # array value
            var_id, vt = self.getVar(ctx.getChild(0).getText(), self.block_number)
            if vt != var_type:
                raise TypeError("wrong type '%s'" % ctx.getText())
            arr_index = ctx.getChild(2)
            self._add_ins('aload %s' % var_id)
            self.calculateExpression(arr_index, 'int')
            self._add_ins('aload', var_type)

        elif ctx.getChildCount() == 3:  # expr
            if ctx.getChild(0).getText() == '(':
                self.calculateExpression(ctx.getChild(1), var_type)
            else:
                i1, o, i2 = ctx.getChildren()
                o = o.getText()

                self.calculateExpression(i1, var_type)
                self.calculateExpression(i2, var_type)
                if o == '+':
                    self._add_ins("add", var_type)
                elif o == '-':
                    self._add_ins("sub", var_type)
                elif o == '*':
                    self._add_ins("mul", var_type)
                elif o == '/':
                    self._add_ins("div", var_type)

    def getLastChild(self, ctx):
        if ctx.getChildCount() == 0 or ctx.getChildCount() > 1:
            return ctx
        return self.getLastChild(ctx.getChild(0))

    def newLabel(self):
        self.label_number += 1
        return "label_%s" % self.label_number

    def enterStatement(self, ctx):
        statement_type = ctx.getRuleIndex()

        if statement_type == pccParser.RULE_selectionStatement:
            self.enterSelectionStatement(ctx)

        elif statement_type == pccParser.RULE_iterationStatement:
            self.enterIterationStatement(ctx)

        elif statement_type == pccParser.RULE_labeledStatement:
            self.enterLabeledStatement(ctx)

    def enterSelectionStatement(self, ctx):
        selection_type = ctx.getChild(0).getSymbol().type

        if selection_type == pccLexer.If:
            self.calculateExpression(ctx.getChild(2), 'int')
            label = self.newLabel()
            self._add_ins("ifeq %s" % label)
            self.enterStatement(ctx.getChild(4))
            self._add_ins("%s:" % label)

        elif selection_type == pccLexer.Switch:
            pass

