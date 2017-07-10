from pccListener import pccListener
from error_listener import NotDeclaredException, RedeclarationException
from pccLexer import pccLexer
from pccParser import pccParser


class pccPrintListener(pccListener):
    def __init__(self, name):
        super(pccPrintListener, self).__init__()
        self.code = "" # bytecode
        self.name = name
        self.block_number = 0
        self.variable_number = 1
        self.label_number = 0
        self.classes = {}
        self.class_arrays = {}
        self.field_table = {}
        self.variable_table = {}
        self.var_type_table = {
            'int': 'i',
            'float': 'f',
            'double': 'd',
            'long': 'l',
            'char': 'i'
        }
        self.desc_var_type_table = {
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
        if (name, self.block_number) in self.variable_table:
            raise RedeclarationException(name)
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


    def newLabel(self):
        self.label_number += 1
        return "label_%s" % self.label_number


    def lastLabel(self):
        return "label_%s" % self.label_number


    def getType(self, ctx):
        ctx = self.getLastChild(ctx)
        if ctx.getSymbol().type == pccLexer.Identifier: # identifier
            var_id, vt = self.getVar(ctx.getText(), self.block_number)
            return vt
        text = ctx.getText().lower()
        if text.endswith('l'):
            return 'long'
        if '.' in text:
            return 'double'
        if text.endswith('f') and '.' in text:
            return 'float'
        if text.startswith('\''):
            return 'char'
        return 'int'


    def getBytecode(self):
        return self.code, self.classes


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


    def _add_class_ins(self, class_name, instruction):
        if not class_name in self.classes:
            self.classes[class_name] = ''
        self.classes[class_name] += instruction + '\n'


    def _create_class(self, class_name, fields):
        self._add_class_ins(class_name, '.class %s' % class_name)
        self._add_class_ins(class_name, '.super java/lang/Object')

        arrays = []
        field_table = {}

        for field_name, field_type in fields:
            field_table[field_name] = field_type
            if isinstance(field_type, tuple):
                array_type, array_size = field_type
                desc = '[' + self.desc_var_type_table[array_type]
                arrays.append((field_name, array_type, array_size, desc))
            else:
                desc = self.desc_var_type_table[field_type]
            self._add_class_ins(class_name, '.field public %s %s' % 
                    (field_name, desc))

        self._add_class_ins(class_name, '.method <init>()V')
        self._add_class_ins(class_name, 'aload_0')
        self._add_class_ins(class_name, 'invokespecial java/lang/Object/<init>()V')

        self._add_class_ins(class_name, 'return')
        self._add_class_ins(class_name, '.end method')

        self.class_arrays[class_name] = arrays
        self.field_table[class_name] = field_table


    def enterCompoundStatement(self, ctx):
        self.block_number += 1

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

        self._add_ins("invokevirtual java/io/PrintStream/println(%s)V" % self.desc_var_type_table[var_type])


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


    def enterPrintStatement(self, ctx):
        var_type = ctx.getChild(4).getText()
        self._add_ins("getstatic java/lang/System/out Ljava/io/PrintStream;")
        self.calculateExpression(ctx.getChild(2), var_type)
        self._add_ins("invokevirtual java/io/PrintStream/println(%s)V" % self.desc_var_type_table[var_type])


    def enterDeclaration(self, ctx):
        if ctx.getText().startswith('struct'): # struct defination
            if self.getLastChild(ctx.getChild(0)).getChildCount() == 4: # create class
                spec_list, class_name, _ = list(ctx.getChildren())
                class_name = class_name.getText()
                spec_list = self.getLastChild(spec_list).getChild(-2)
                fields = self.getClassFields(spec_list)
                self._create_class(class_name, fields)

            elif self.getLastChild(ctx.getChild(0)).getChildCount() == 2: # create instance
                class_name = self.getLastChild(ctx.getChild(0)).getChild(1).getText()
                var_id = self.newVar(ctx.getChild(1).getText(), class_name)
                self._add_ins("new %s" % class_name)
                self._add_ins("dup")
                self._add_ins("invokespecial %s.<init>()V" % class_name)
                self._add_ins("astore %s" % var_id)

                # initialize arrays
                for name, atype, size, desc in self.class_arrays[class_name]:
                    self._add_ins("aload %s" % var_id)
                    self._add_ins('ldc %s' % size)
                    self._add_ins('newarray %s' % atype)
                    self._add_ins('putfield %s.%s %s' % (class_name, name, desc))

        elif ctx.getChildCount() == 3: # variable declration
            var_type, ids, _ = list(ctx.getChildren())
            var_type = var_type.getText()

            for child in ids.getChildren():
                if child.getText() == ',':
                    continue
                c = child.getChild(0)
                c = self.getLastChild(child)
                c_count = c.getChildCount()

                if c_count == 0 or c_count == 3: # var
                    var_id = self.newVar((c.getChild(0) if c_count == 3 else c).getText(), var_type)
                    self._push_constant(0, var_type)
                    self._add_ins("store %s" % var_id, var_type)

                elif c_count == 4: # array
                    var_id = self.newVar(c.getChild(0).getText(), var_type)
                    size = c.getChild(2).getText()
                    self._add_ins("ldc %s" % size)
                    self._add_ins("newarray %s" % var_type)
                    self._add_ins("astore %s" % var_id)

                if c_count == 3: # declration with assignment
                    self.enterAssignmentExpression(c)


    def enterAssignmentExpression(self, ctx):
        if ctx.getChildCount() == 3:
            assignee, _, value = list(ctx.getChildren())
            assignee = self.getLastChild(assignee)
            if assignee.getChildCount() == 0: # identifier
                var_id, var_type = self.getVar(assignee.getText(), self.block_number)
                self.calculateExpression(value, var_type)
                self._add_ins("store %s" % var_id, var_type)

            elif assignee.getChildCount() == 4: # array
                var_id, var_type = self.getVar(assignee.getChild(0).getText(), self.block_number)
                index = assignee.getChild(2)
                self._add_ins('aload %s' % var_id)
                self.calculateExpression(index, 'int')
                self.calculateExpression(value, var_type)
                self._add_ins('astore', var_type)

            elif assignee.getChildCount() == 3: # struct
                identifier, _, field = list(assignee.getChildren())
                field = field.getText()
                var_id, class_name = self.getVar(identifier.getText(), self.block_number)
                var_type = self.field_table[class_name][field]
                desc = self.desc_var_type_table[var_type]
                self._add_ins("aload %s" % var_id)
                self.calculateExpression(value, var_type)
                self._add_ins('putfield %s.%s %s' % (class_name, field, desc))


    def enterSelectionStatement(self, ctx):
        selection_type = ctx.getChild(0).getSymbol().type

        if selection_type == pccLexer.If:
            self.calculateCondExpression(ctx.getChild(2))
            label = self.newLabel()
            self._add_ins("ifeq %s" % label)

        elif selection_type == pccLexer.Switch:
            pass


    def exitSelectionStatement(self, ctx):
        self._add_ins("%s:" % self.lastLabel())


    def calculateCondExpression(self, ctx):

        def compare(cmd, op1, op2):
            t = self.getType(op1)
            if t != self.getType(op2):
                raise TypeError("wrong type '%s' and '%s'" % (op1.getText(), op2.getText()))
            self.calculateExpression(op1, t)
            self.calculateExpression(op2, t)
            self._add_ins('sub', t)

            label1 = self.newLabel()
            label2 = self.newLabel()
            self._add_ins('if%s %s' % (cmd, label1))
            self._add_ins('bipush 0')
            self._add_ins('goto %s' % label2)
            self._add_ins("%s:" % label1)
            self._add_ins('bipush 1')
            self._add_ins("%s:" % label2)

        c = self.getLastChild(ctx)
        if c.getChild(0).getText() == '(':
            self.calculateCondExpression(c.getChild(1))
            return

        op1, opr, op2 = list(c.getChildren())
        if opr.getText() == '==':
            compare('eq', op1, op2)
        elif opr.getText() == '>=':
            compare('ge', op1, op2)
        elif opr.getText() == '>':
            compare('gt', op1, op2)
        elif opr.getText() == '<=':
            compare('le', op1, op2)
        elif opr.getText() == '<':
            compare('lt', op1, op2)
        elif opr.getText() == '!=':
            compare('ne', op1, op2)

        elif opr.getText() == '&&':
            self.calculateCondExpression(op1)
            self.calculateCondExpression(op2)
            self._add_ins('iadd')
            self._add_ins('bipush 2')
            self._add_ins('isub')

            label1 = self.newLabel()
            label2 = self.newLabel()
            self._add_ins('ifeq %s' % (label1))
            self._add_ins('bipush 0')
            self._add_ins('goto %s' % label2)
            self._add_ins("%s:" % label1)
            self._add_ins('bipush 1')
            self._add_ins("%s:" % label2)

        elif opr.getText() == '||':
            self.calculateCondExpression(op1)
            self.calculateCondExpression(op2)
            self._add_ins('iadd')

            label1 = self.newLabel()
            label2 = self.newLabel()
            self._add_ins('ifgt %s' % (label1))
            self._add_ins('bipush 0')
            self._add_ins('goto %s' % label2)
            self._add_ins("%s:" % label1)
            self._add_ins('bipush 1')
            self._add_ins("%s:" % label2)



    def calculateExpression(self, ctx, var_type):
        ctx = self.getLastChild(ctx)

        if ctx.getChildCount() == 0: # identifier or constant value
            if ctx.getSymbol().type == pccLexer.Identifier: # identifier
                var_id, vt = self.getVar(ctx.getText(), self.block_number)
                if vt != var_type:
                    raise TypeError("wrong type '%s'" % ctx.getText())
                self._add_ins("load %s" % var_id, var_type)
            else: # constant value
                self._push_constant(ctx.getText(), var_type)

        if ctx.getChildCount() == 4: # array value
            var_id, vt = self.getVar(ctx.getChild(0).getText(), self.block_number)
            if vt != var_type:
                raise TypeError("wrong type '%s'" % ctx.getText())
            arr_index = ctx.getChild(2)
            self._add_ins('aload %s' % var_id)
            self.calculateExpression(arr_index, 'int')
            self._add_ins('aload', var_type)

        elif ctx.getChildCount() == 3: # expr
            if ctx.getChild(0).getText() == '(':
                self.calculateExpression(ctx.getChild(1), var_type)
            elif ctx.getChild(1).getText() == '.':
                identifier, _, field = list(ctx.getChildren())
                field = field.getText()
                var_id, class_name = self.getVar(identifier.getText(), self.block_number)
                var_type = self.field_table[class_name][field]
                desc = self.desc_var_type_table[var_type]
                self._add_ins("aload %s" % var_id)
                self._add_ins('getfield %s.%s %s' % (class_name, field, desc))
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
                elif o == '%':
                    self._add_ins("rem", var_type)


    def getLastChild(self, ctx):
        if ctx.getChildCount() == 0 or ctx.getChildCount() > 1:
            return ctx
        return self.getLastChild(ctx.getChild(0))


    def getClassFields(self, spec_list):
        fields = []
        for spec in spec_list.getChildren():
            spec = self.getLastChild(spec)
            if spec.getChildCount() == 2:
                fields += self.getClassFields(spec_list.getChild(0))
            elif spec.getChildCount() == 3:
                var_type = spec.getChild(0).getText()
                for identifier in spec.getChild(1).getChildren():
                    identifier = self.getLastChild(identifier)
                    if identifier.getText() == ',':
                        continue
                    if identifier.getChildCount() == 0:
                        fields.append((identifier.getText(), var_type))
                    elif identifier.getChildCount() == 4:
                        name, _, size, _ = identifier.getChildren()
                        fields.append((name.getText(), (var_type, size.getText())))
        return fields
