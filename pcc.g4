grammar pcc;

// ======================  Rules ======================

primaryExpression
    :   Identifier
    |   Constant
    |   StringLiteral+
    |   '(' expression ')'
    ;

postfixExpression
    :   primaryExpression
    |   postfixExpression '[' expression ']'
    |   postfixExpression '(' argumentExpressionList? ')'
    | postfixExpression '.' Identifier
    |   '(' typeName ')' '{' initializerList '}'
    |   '(' typeName ')' '{' initializerList ',' '}'
    ;

argumentExpressionList
    :   assignmentExpression
    |   argumentExpressionList ',' assignmentExpression
    ;

unaryExpression
    :   postfixExpression
    |   unaryOperator castExpression
    ;

unaryOperator
    : '+' | '-' | '!'
    ;

castExpression
    :   unaryExpression
    |   '(' typeName ')' castExpression
    ;

multiplicativeExpression
    :   castExpression
    |   multiplicativeExpression '*' castExpression
    |   multiplicativeExpression '/' castExpression
    |   multiplicativeExpression '%' castExpression
    ;

additiveExpression
    :   multiplicativeExpression
    |   additiveExpression '+' multiplicativeExpression
    |   additiveExpression '-' multiplicativeExpression
    ;

relationalExpression
    :   additiveExpression
    |   relationalExpression '<' additiveExpression
    |   relationalExpression '>' additiveExpression
    |   relationalExpression '<=' additiveExpression
    |   relationalExpression '>=' additiveExpression
    ;

equalityExpression
    :   relationalExpression
    |   equalityExpression '==' relationalExpression
    |   equalityExpression '!=' relationalExpression
    ;

logicalAndExpression
    :   equalityExpression
    |   logicalAndExpression '&&' equalityExpression
    ;

logicalOrExpression
    :   logicalAndExpression
    |   logicalOrExpression '||' logicalAndExpression
    ;

assignmentExpression
    :   logicalOrExpression
    |   unaryExpression '=' assignmentExpression
    ;

expression
    :   assignmentExpression
    |   expression ',' assignmentExpression
    ;

constantExpression
    :   logicalOrExpression
    ;

declaration
    :   declarationSpecifiers initDeclaratorList ';'
	| 	declarationSpecifiers ';'
    ;

declarationSpecifiers
    :   declarationSpecifier+
    ;

declarationSpecifiers2
    :   declarationSpecifier+
    ;

declarationSpecifier
    :   storageClassSpecifier
    |   typeSpecifier
    |   typeQualifier
    ;

initDeclaratorList
    :   initDeclarator
    |   initDeclaratorList ',' initDeclarator
    ;

initDeclarator
    :   declarator
    |   declarator '=' initializer
    ;

storageClassSpecifier
    :   'static'
    ;

typeSpecifier
    :   ('void'
    |   'char'
    |   'short'
    |   'int'
    |   'long'
    |   'float'
    |   'double'
    |   'signed'
    |   'unsigned')
    |   structOrUnionSpecifier
    |   enumSpecifier
    ;

structOrUnionSpecifier
    :   structOrUnion Identifier? '{' structDeclarationList '}'
    |   structOrUnion Identifier
    ;

structOrUnion
    :   'struct'
    |   'union'
    ;

structDeclarationList
    :   structDeclaration
    |   structDeclarationList structDeclaration
    ;


structDeclaration
    :   specifierQualifierList structDeclaratorList? ';'
    ;

specifierQualifierList
    :   typeSpecifier specifierQualifierList?
    |   typeQualifier specifierQualifierList?
    ;

structDeclaratorList
    :   structDeclarator
    |   structDeclaratorList ',' structDeclarator
    ;

structDeclarator
    :   declarator
    |   declarator? ':' constantExpression
    ;

enumSpecifier
    :   'enum' Identifier? '{' enumeratorList '}'
    |   'enum' Identifier? '{' enumeratorList ',' '}'
    |   'enum' Identifier
    ;

enumeratorList
    :   enumerator
    |   enumeratorList ',' enumerator
    ;

enumerator
    :   enumerationConstant
    |   enumerationConstant '=' constantExpression
    ;

enumerationConstant
    :   Identifier
    ;

typeQualifier
    :   'const'
    ;

declarator
    :   directDeclarator
    ;

directDeclarator
    :   Identifier
    |   '(' declarator ')'
    |   directDeclarator '[' typeQualifier? assignmentExpression? ']'
    |   directDeclarator '[' 'static' typeQualifier? assignmentExpression ']'
    |   directDeclarator '[' typeQualifier 'static' assignmentExpression ']'
    |   directDeclarator '[' typeQualifier? '*' ']'
    |   directDeclarator '(' parameterTypeList ')'
    |   directDeclarator '(' identifierList? ')'
    ;

nestedParenthesesBlock
    :   (   ~('(' | ')')
        |   '(' nestedParenthesesBlock ')'
        )*
    ;

parameterTypeList
    :   parameterList
    ;

parameterList
    :   parameterDeclaration
    |   parameterList ',' parameterDeclaration
    ;

parameterDeclaration
    :   declarationSpecifiers declarator
    |   declarationSpecifiers2 abstractDeclarator?
    ;

identifierList
    :   Identifier
    |   identifierList ',' Identifier
    ;

typeName
    :   specifierQualifierList abstractDeclarator?
    ;

abstractDeclarator
    :   directAbstractDeclarator
    ;

directAbstractDeclarator
    :   '(' abstractDeclarator ')'
    |   '[' typeQualifier? assignmentExpression? ']'
    |   '[' 'static' typeQualifier? assignmentExpression ']'
    |   '[' typeQualifier 'static' assignmentExpression ']'
    |   '(' parameterTypeList? ')'
    |   directAbstractDeclarator '[' typeQualifier? assignmentExpression? ']'
    |   directAbstractDeclarator '[' 'static' typeQualifier? assignmentExpression ']'
    |   directAbstractDeclarator '[' typeQualifier 'static' assignmentExpression ']'
    |   directAbstractDeclarator '(' parameterTypeList? ')'
    ;

initializer
    :   assignmentExpression
    |   '{' initializerList '}'
    |   '{' initializerList ',' '}'
    ;

initializerList
    :   designation? initializer
    |   initializerList ',' designation? initializer
    ;

designation
    :   designatorList '='
    ;

designatorList
    :   designator
    |   designatorList designator
    ;

designator
    :   '[' constantExpression ']'
    |   '.' Identifier
    ;

statement
    :   labeledStatement
    |   compoundStatement
    |   expressionStatement
    |   selectionStatement
    |   iterationStatement
    |   jumpStatement
    |   printStatement
    ;

labeledStatement
    :   Identifier ':' statement
    |   'case' constantExpression ':' statement
    |   'default' ':' statement
    ;

compoundStatement
    :   '{' blockItemList? '}'
    ;

blockItemList
    :   blockItem
    |   blockItemList blockItem
    ;

blockItem
    :   declaration
    |   statement
    ;

expressionStatement
    :   expression? ';'
    ;

selectionStatement
    :   'if' '(' expression ')' statement ('else' statement)?
    |   'switch' '(' expression ')' statement
    ;

iterationStatement
    :   'while' '(' expression ')' statement
    |   'for' '(' expression? ';' expression? ';' expression? ')' statement
    |   'for' '(' declaration expression? ';' expression? ')' statement
    ;

jumpStatement
    :   'continue' ';'
    |   'break' ';'
    |   'return' expression? ';'
    ;

printStatement
    :   'printf' '(' primaryExpression ',' typeSpecifier ')' ';'
    ;

program
    :   translationUnit? EOF
    ;

translationUnit
    :   externalDeclaration
    |   translationUnit externalDeclaration
    ;

externalDeclaration
    :   functionDefinition
    |   declaration
    |   ';' // stray ;
    ;

functionDefinition
    :   declarationSpecifiers? declarator declarationList? compoundStatement
    ;

declarationList
    :   declaration
    |   declarationList declaration
    ;

// ====================== Tokens ======================

Break: 'break';
Case: 'case';
Char: 'char';
Const: 'const';
Continue: 'continue';
Default: 'default';
Double: 'double';
Else: 'else';
Enum: 'enum';
Float: 'float';
For: 'for';
If: 'if';
Int: 'int';
Long: 'long';
Return: 'return';
Short: 'short';
Signed: 'signed';
Static: 'static';
Struct: 'struct';
Switch: 'switch';
Union: 'union';
Unsigned: 'unsigned';
Void: 'void';
While: 'while';

PO: '(';
PC: ')';
BO: '[';
BC: ']';
AO: '{';
AC: '}';

GR: '>';
LR: '<';
GE: '>=';
LE: '<=';

Plus: '+';
Minus: '-';
Mul: '*';
Div: '/';

And: '&&';
Or: '||';
Not: '!';

Colon: ':';
Semi: ';';
Comma: ',';

Assign: '=';

Equal: '==';
NotEqual: '!=';

Dot : '.';

Identifier
    : Letter (Letter | Digit)*
    ;

fragment
Letter
    : [a-zA-Z_]
    ;

fragment
Digit
    : [0-9]
    ;


Constant
    : IntegerConstant
    | FloatingConstant
    | CharacterConstant
    ;

fragment
IntegerConstant
    : (NonzeroDigit Digit*)
    | Zero
    ;

fragment
NonzeroDigit
    : [1-9]
    ;

fragment
Zero
    : '0'
    ;

fragment
FloatingConstant
    : DigitSequence? '.' DigitSequence
    | DigitSequence '.'
    ;

fragment
DigitSequence
    : Digit+
    ;

fragment
CharacterConstant
    :  '\'' (CChar+)? '\''
    ;

fragment
CChar
    : ~['\\\r\n]
    | EscapeSequence
    ;

fragment
EscapeSequence
    : '\\' ['"?abfnrtv\\]
    ;


StringLiteral
    : '"' (SChar+)? '"'
    ;

fragment
SChar
    : ~["\\\r\n]
    | EscapeSequence
    | '\\\n'
    | '\\\r\n'
    ;


Whitespace
    : [ \t]+ -> skip
    ;

Newline
    : ('\r' '\n'? | '\n') -> skip
    ;

BlockComment
    :'/*' .*? '*/' -> skip
    ;

LineComment
    : '//' ~[\r\n]* -> skip
    ;
