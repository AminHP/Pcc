grammar pcc;

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


Id: Letter (Letter | Digit)*;

fragment Letter: [a-zA-Z_];
fragment Digit: [0-9];


Constant: IntegerConstant | FloatingConstant | CharacterConstant;

fragment IntegerConstant: NonzeroDigit Digit*;
fragment NonzeroDigit: [1-9];

fragment FloatingConstant: DigitSequence? '.' DigitSequence | DigitSequence '.';
fragment DigitSequence: Digit+;

fragment CharacterConstant:  ~['\\\r\n] | EscapeSequence;
fragment EscapeSequence: '\\' ['"?abfnrtv\\];


StringLiteral: '"' (SCharSequence+)? '"';

fragment SCharSequence: ~["\\\r\n] |   EscapeSequence | '\\\n' | '\\\r\n';


Whitespace: [ \t]+ -> skip;
Newline: ('\r' '\n'? | '\n') -> skip;
BlockComment :'/*' .*? '*/' -> skip;
LineComment : '//' ~[\r\n]* -> skip;


// ======================  Rules ======================

int_dec: Int Id (Assign Constant)? Semi;
float_dec: Float Id (Assign Constant)? Semi;
char_dec: Char Id (Assign Constant)? Semi;
decs: int_dec | float_dec | char_dec;

program: (decs)*;
