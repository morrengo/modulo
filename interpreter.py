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
		elif(node.node_type == 'print'):
			print eval(node.children[0])
		else:
			raise Exception("unsupported expression type \'"+node.node_type+"\'")
	except Exception as e:
		print str(e)

s = '''
% MyMod{
	a=3;
	c=a+3;
	print c;
	c= c/4.0;
	c=c*5;
	b = 2;
	a= (b+1.0)*2+1.3;
	print c+a;
}
'''
node = parser.parse(s)
#node.print_node()
eval(node)
