grammar pcc;

///////////////////// Token /////////////////////

WS:
	(' ' | '\t' | '\n')+
	-> skip;

Comment:
	(('//' ~[\r\n]*) | ('/*' .*? '*/'))
	-> skip;


Assign: '=';
Not: '!';
Equal: '==';
NotEqual: '!=';
GR: '>';
LR: '<';
GE: '>=';
LE: '<=';
Plus: '+';
Minus: '-';
Mul: '*';
Div: '/';

PO: '(';
PC: ')';
AO: '{';
AC: '}';
BO: '[';
BC: ']';

Colon: ':';
Semi: ';';
Comma: ',';

IntKW: 'int';
FloatKW: 'float';
CharKW: 'char';
StringKW: 'string';
BoolKW: 'bool';
VoidKW: 'void';

IntVal: (Plus | Minus)? Digit+;
FloatVal: (Plus | Minus)? Digit+ '.' Digit+;
CharVal: '\'' ~('\'') '\'';
StringVal: '"' ~('\r' | '\n' | '"')* '"';


fragment Underscore: '_';
fragment Letter: [a-zA-Z];
fragment Digit: [0-9];

Id: (Letter | Underscore) (Letter | Underscore | Digit)*;


// ********************* Rules *********************

int_dec: IntKW Id (Assign IntVal)? Semi;
float_dec: FloatKW Id (Assign FloatVal)? Semi;
char_dec: CharKW Id (Assign CharVal)? Semi;
string_dec: StringKW Id (Assign StringVal)? Semi;
decs: int_dec | float_dec | char_dec | string_dec;

program: (decs)*;
