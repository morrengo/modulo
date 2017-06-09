import ply.lex as lex

reserved = {
	'print' : 'PRINT',
    'if' 	: 'IF',
    'else' 	: 'ELSE',
	'int' 	: 'INT_TYPE',
	'double': 'DOUBLE_TYPE',
	'char'	: 'CHAR_TYPE',
	'void' 	: 'VOID_TYPE'
}
tokens = 	['MODULO', 'INT', 'DOUBLE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'AND', 'OR', 'EQUALS', 'ASSIGN',
			'BRACE_OPEN', 'BRACE_CLOSE', 'ROUND_OPEN', 'ROUND_CLOSE', 'ARR_OPEN', 'ARR_CLOSE',
			'SEMICOLON', 'ID'] +  list(reserved.values())
t_ignore 		=' \t\n'
t_MODULO		=r'%'
t_DOUBLE		=r'(\d\.\d*)|([1-9]\d*\.\d*)'
t_INT			=r'([1-9]\d*)|(\d)'
t_PLUS			=r'\+'
t_MINUS			=r'-'
t_TIMES			=r'\*'
t_DIVIDE		=r'/'
t_AND			=r'&&'
t_OR 			=r'\|\|'
t_ASSIGN		=r'='
t_EQUALS		=r'=='
t_BRACE_OPEN	=r'{'
t_BRACE_CLOSE	=r'}'
t_ROUND_OPEN	=r'\('
t_ROUND_CLOSE	=r'\)'
t_ARR_OPEN		=r'\['
t_ARR_CLOSE		=r'\]'
t_SEMICOLON		=r';'
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

'''lex.input("x=2-2*2*5 if ")
while True:
	tok = lex.token()
	if not tok: break
	print (tok.type + " : " + tok.value )'''