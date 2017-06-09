import parser
scopes = []
curr_scope={}
node_types=["module","print","assign","declare","decl_type","+","-","*","/","int","double","id"]
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
	if(node.node_type == "module"):
		push_scope()
		for child in node.children
			eval(child)
		pop_scope()
	if(node.node_type == "assign"):
		

s = '''
% MyMod{
	int x = 5;
	int y = x*3;
	int c = x+y;
	c = (c*x)+(x-y);
	print c*a+(2*2);
}
'''

node = parser.parse(s)
