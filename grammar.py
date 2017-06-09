import sys
import ply.yacc as yacc
import tokenizer
tokens = tokenizer.tokens
scopes = []
curr_scope={}

class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf

def push_scope():
	global curr_scope,scopes
	scopes.append(dict(curr_scope))
	curr_scope={}

def add_to_scope(definition,value):
	curr_scope[definition]=value

def get_from_scope(definition):
	return curr_scope[definition]

def pop_scope():
	global curr_scope
	curr_scope = scopes.pop()

def push_scope():
	curr_scope = []
	scopes.append(curr_scope)

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def p_module(p):
	'''module : moduloB ID body'''
def p_moduloB(p):
	'''moduloB : MODULO'''	
	push_scope()

def p_body(p):
	'''body : BRACE_OPEN lines BRACE_CLOSE'''

def p_lines(p):
	'''lines : line lines
			 | line'''

def p_line(p):
	'''line : assignment SEMICOLON
			| declare SEMICOLON'''
# def p_line(p):
# 	'''line : ID ASSIGN expr SEMICOLON SEMICOLON
# 			| declare SEMICOLON'''
# 	if len(p) >3:
# 		if p[1] in curr_scope:
# 			add_to_scope(p[1],p[3])
# 		else:
# 			print "variable","\'"+p[1]+"\'","not in scope"
# 			raise SyntaxError

def p_assignment(p):
	'''assignment : ID ASSIGN expr'''
	if p[1] in curr_scope:
		add_to_scope(p[1],p[3])
	else:
		print "variable","\'"+p[1]+"\'","not in scope"
		raise SyntaxError

def p_declare(p):
	'''declare : type ID
			   | type ID ASSIGN expr'''
	if len(p) <= 3 :
		add_to_scope(p[2],None)
	else :
		add_to_scope(p[2],p[4])

def p_type(p):
	'''type : INT_TYPE
			| DOUBLE_TYPE
			| CHAR_TYPE
			| VOID_TYPE'''
def p_expr_group(p):
   '''expr : ROUND_OPEN expr ROUND_CLOSE'''
   p[0] = p[2]

def p_expr(p):
	'''expr : expr PLUS term
			| expr MINUS term'''
	if(p[2] == '-'):
		p[0] = p[1] - p[3]
	if(p[2] == '+'):
		p[0] = p[1] + p[3]

def p_expr_term(p):
	'''expr : term'''
	p[0] = p[1]

def p_term(p):
	'''term : term TIMES factor
			| term DIVIDE factor'''
	if(p[2] == '*'):
		p[0] = p[1] * p[3]
	if(p[2] == '/'):
		p[0] = p[1] / p[3]

def p_term_factor(p):
	'''term : factor'''
	p[0] = p[1]

def p_factorInt(p):
	'''factor : INT'''
	p[0] = int(p[1])

def p_factorDouble(p):
	'''factor : DOUBLE'''
	p[0] = float(p[1])

def p_factorID(p):
	'''factor : ID'''	
	if p[1] in curr_scope:
		p[0] = get_from_scope(p[1])
	else:
		print "variable","\'"+p[1]+"\'","not in scope"
		raise SyntaxError

def p_factorExpr(p):
	'''factor : expr'''	
	p[0] = p[1]		

def p_expr_uminus(t):
    '''expr : MINUS expr %prec UMINUS'''
    t[0] = -t[2]

def p_error(t):
    print("Syntax error at: \""+ t.value+"\" in "+ str(t.lexpos) )

def p_empty(p):
    'empty :'
    pass

import ply.yacc as yacc
yacc.yacc(debug=True)
'''if len(sys.argv) > 1:
	s = sys.argv
	print s[1]
	with open(s[1], 'r') as myfile:
		data=myfile.read().replace('\n', '')
	print (yacc.parse(data))
else:
	print "no file name specified in arguments"'''



#print (yacc.parse(s))
def parse(s):
	return yacc.parse(s)