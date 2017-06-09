scopes = []
curr_scope={}

def push_scope():
	global curr_scope,scopes
	scopes.append(dict(curr_scope))
	curr_scope={}

def add_to_scope(definition,value):
	curr_scope[definition]=value

def pop_scope():
	global curr_scope
	curr_scope = scopes.pop()
