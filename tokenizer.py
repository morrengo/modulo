import ply.lex as lex
tokens = 	['ID', 'INT', 'DOUBLE', 'PLUS', 'MINUS', 'MULT', 'DIV', 'AND', 'OR', 'EQUALS', 'ASSIGN',
			'BRACE_OPEN', 'BRACE_CLOSE', 'ROUND_OPEN', 'ROUND_CLOSE', 'ARR_OPEN', 'ARR_CLOSE',
			'IF', 'ELSE']
t_ignore 		=' \t'
t_ID 			=r'[a-zA-Z][a-zA-Z0-9]*'
t_DOUBLE		=r'-?(\d\.\d*)|([1-9]\d*\.\d*)'
t_INT			=r'-?([1-9]\d*)|(\d)'
t_PLUS			=r'\+'
t_MINUS			=r'-'
t_MULT			=r'\*'
t_DIV			=r'/'
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
t_IF			=r'if'
r_ELSE			=r'else'
lex.lex()

lex.input("x=[---2.5*2]{==}+(-3)*3")
while True:
	tok = lex.token()
	if not tok: break
	print (tok.type + " : " + tok.value )