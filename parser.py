import sys
import ply.yacc as yacc
import tokenizer
tokens = tokenizer.tokens
ident=" "
class Node:

    def __init__(self,node_type,children=None,info=None):
        self.node_type = node_type
        if children:
             self.children = children
        else:
             self.children = []
        self.info = info

    def print_node(self):
    	global ident
    	if(self.children == []):
    		print ident,self.node_type,":",self.info
    	else:
    		print ident,self.node_type,"->",self.info
    		for child in self.children:
    			ident = ident+"  "
    			if isinstance(child, Node):
    				child.print_node()
    			ident = ident[:-2]

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def p_module(p):
	'''module : MODULO ID body'''
	p[0] = Node('module',p[3],p[2])

def p_body(p):
	'''body : BRACE_OPEN lines BRACE_CLOSE'''
	p[0] = p[2]

def p_lines(p):
	'''lines : line lines
			 | line'''
	if len(p) > 2 :
		p[0] = [p[1]]+p[2]
	else :
		p[0] = [p[1]]

# def p_line(p):
# 	'''line : assign SEMICOLON
# 			| print SEMICOLON
# 			| if
# 			| while'''
# 	p[0] = p[1]

def p_line(p):
	'''line : assign SEMICOLON
			| print SEMICOLON'''
	p[0] = p[1]

def p_print(p):
	'''print : PRINT expr'''
	p[0] = Node('print',[p[2]])

def p_assign(p):
    '''assign : identifier ASSIGN expr'''
    p[0] = Node('assign',[p[1]]+[p[3]])

def p_expr_group(p):
   '''expr : ROUND_OPEN expr ROUND_CLOSE'''
   p[0] = p[2]

def p_expr(p):
	'''expr : expr PLUS term
			| expr MINUS term'''
	p[0] = Node(p[2],[p[1]]+[p[3]])

def p_expr_term(p):
	'''expr : term'''
	p[0] = p[1]

def p_term(p):
	'''term : term TIMES factor
			| term DIVIDE factor'''
	p[0] = Node(p[2],[p[1]]+[p[3]])

def p_term_factor(p):
	'''term : factor'''
	p[0] = p[1]

def p_factorInt(p):
	'''factor : INT'''
	p[0] = Node('int',None,p[1])

def p_factorDouble(p):
	'''factor : DOUBLE'''
	p[0] = Node('double',None,p[1])

def p_factorID(p):
	'''factor : identifier'''
	p[0] = p[1]

def p_factorExpr(p):
	'''factor : expr'''	
	p[0] = p[1]		

def p_identifier(p):
	'''identifier : ID'''
	p[0] = Node('id',None,p[1])

# def p_if(p):
# 	'''if : IF ROUND_OPEN condition ROUND_CLOSE if_body'''
# 	p[0] = Node('if',[p[3]]+p[5])

# def p_if_body(p):
# 	'''if_body : body 
# 			   | '''

def p_expr_uminus(t):
    '''expr : MINUS expr %prec UMINUS'''
    t[0] = -t[2]

def p_error(t):
    print("Syntax error before: \""+ t.value+"\" in "+ str(t.lexpos) )

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


s = '''
% MyMod{
	a=1;
	print x;
	x = 2 * a + 3;
}
'''
#node= (yacc.parse(s))
#node.print_node()

def parse(s):
	return (yacc.parse(s))