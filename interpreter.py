import parser
scopes = []
curr_scope={}
node_types=["module","print","assign","declare","decl_type",
	"+","-","*","/","int","double","id"]
def push_scope():
	global curr_scope,scopes
	scopes.append(dict(curr_scope))
	curr_scope={}

def add_to_scope(definition,value):
	curr_scope[definition]=value

def pop_scope():
	global curr_scope
	curr_scope = scopes.pop()

def get_from_scope(definition):
	try:
		return curr_scope[definition]
	except:
		return None

def eval(node):
	try:
		if(node.node_type == "module"):
			push_scope()
			for child in node.children:
				eval(child)
			pop_scope()
		elif(node.node_type == "assign"):
			target = node.children[0]
			expression = node.children[1]
			val = eval(expression)
			add_to_scope(target.info, val)
		elif(node.node_type == '+'):
			return eval(node.children[0]) + eval(node.children[1])
		elif(node.node_type == '-'):
			return eval(node.children[0]) - eval(node.children[1])
		elif(node.node_type == '*'):
			return eval(node.children[0]) * eval(node.children[1])
		elif(node.node_type == '/'):
			return eval(node.children[0]) / eval(node.children[1])
		elif(node.node_type == 'id'):
			val = get_from_scope(node.info)
			if val is not None:
				return get_from_scope(node.info)
			else:
				raise Exception("undefined variable \'"+node.info+"\'")
		elif(node.node_type == 'int'):
			return int(node.info)
		elif(node.node_type == 'double'):
			return float(node.info)
		elif(node.node_type == 'bool_literal'):
			if(node.info == "true"):
				return True
			return False
		elif(node.node_type == 'print'):
			print eval(node.children[0])
		elif(node.node_type == 'or'):
			return eval(node.children[0]) or eval(node.children[1])
		elif(node.node_type == 'and'):
			return eval(node.children[0]) and eval(node.children[1])
		elif(node.node_type == 'not'):
			return not eval(node.children[0])
		elif(node.node_type == '@='):
			return eval(node.children[0]) != eval(node.children[1])
		elif(node.node_type == '=='):
			return eval(node.children[0]) == eval(node.children[1])
		elif(node.node_type == '<'):
			return eval(node.children[0]) < eval(node.children[1])
		elif(node.node_type == '<='):
			return eval(node.children[0]) <= eval(node.children[1])
		elif(node.node_type == '>='):
			return eval(node.children[0]) >= eval(node.children[1])
		elif(node.node_type == '>'):
			return eval(node.children[0]) > eval(node.children[1])
		elif(node.node_type == 'while'):
			while eval(node.children[0])==True :
				for child in node.children[1:]:
					eval(child)
		else:
			raise Exception("unsupported expression type \'"+node.node_type+"\'")
	except Exception as e:
		print str(e)

s = '''
% silnia{
	a=5;
	b=1;
	c=1;
	while (c)<=a{
		b=b*c;
		c = c+1;
	}
	print b;
}
'''
node = parser.parse(s)
node.print_node()
eval(node)
