import parser
import sys
scopes = []
curr_scope={}

node_types=["module","print","assign","declare","decl_type",
	"+","-","*","/","int","double","id"]
def push_scope():
	global curr_scope,scopes
	scopes.append(dict(curr_scope))
	curr_scope={}

def add_to_scope(definition,val):
	curr_scope[definition]=val

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
		if(node.node_type == 'module'):
			push_scope()
			eval(node.children[0])
			pop_scope()
		elif(node.node_type == 'body'):
			for child in node.children:
				eval(child)
		elif(node.node_type == "assign"):
			target = node.children[0]
			expression = node.children[1]
			val = eval(expression)
			add_to_scope(target.info, val)
		elif(node.node_type == "assign_proc"):
			target = node.children[0]
			expression = node.children[1]
			add_to_scope(target.info, expression)
		elif(node.node_type == "procedure"):
			if(isinstance(get_from_scope(node.info),parser.Node)):
				eval(get_from_scope(node.info))
			else:
				raise Exception("\'"+node.info+"\' is not a function or is undefined")
		elif(node.node_type == 'println'):
			if node.children is None or len(node.children)==0:
				print
			else:
				print eval(node.children[0])
		elif(node.node_type == 'print'):
			sys.stdout.write(str(eval(node.children[0])))
		elif(node.node_type == 'while'):
			while eval(node.children[0])==True :
				eval(node.children[1])

		elif(node.node_type == 'if'):
			if( eval(node.children[0]) == True):
				eval(node.children[1])
				return
			if(len(node.children) > 2):
				for child in node.children[2:]:
					if(child.node_type == 'else'):
						eval(child.children[0])
						return
					if(eval(child.children[0]) == True):
						eval(child.children[1])
						return

		elif(node.node_type == '+'):
			return eval(node.children[0]) + eval(node.children[1])
		elif(node.node_type == '-'):
			return eval(node.children[0]) - eval(node.children[1])
		elif(node.node_type == '*'):
			return eval(node.children[0]) * eval(node.children[1])
		elif(node.node_type == '/'):
			return eval(node.children[0]) / eval(node.children[1])

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

		elif(node.node_type == 'id'):
			val = get_from_scope(node.info)
			if val is not None:
				return get_from_scope(node.info)
			else:
				raise Exception("undefined variable \'"+node.info+"\'")
		elif(node.node_type == 'text'):
			return str(node.info)
		elif(node.node_type == 'int'):
			return int(node.info)
		elif(node.node_type == 'double'):
			return float(node.info)
		elif(node.node_type == 'bool_literal'):
			if(node.info == "true"):
				return True
			return False
		elif(node.node_type == 'arr_index'):
			val = eval(node.children[0])
			if(not(isinstance(val,list) or isinstance(val,str))):
				raise Exception("variable \'"+node.children[0]+"\' is not an array")
				return
			index = eval(node.children[1])
			if(not isinstance(index,int)):
				raise Exception("index of array \'"+node.children[0]+"\' is not an integer")
				return
			if(len(val)<=index):
				raise Exception("index of array \'"+node.children[0]+"\' is out of range")
				return
			return val[index]
		elif(node.node_type == 'arr'):
			res = []
			if(node.children == []):
				return res
			for child in node.children:
				res = res + [eval(child)]
			return res
		elif(node.node_type == 'len'):
			val = eval(node.children[0])
			if(not(isinstance(val,list) or isinstance(val,str))):
				raise Exception("variable \'"+node.children[0]+"\' is not an array")
				return
			return len(val)
		else:
			raise Exception("unsupported expression type \'"+node.node_type+"\'")
	except Exception as e:
		print str(e)

s1 = '''
% silnia{
	wyswietl_ukosnie = {
		c=0;
		while c < len napis {
			a=0;
			while a < c {
				print " ";
				a = a+1;
			}
			print napis[c];
			c = c+1;
			println;
		}
	};

	napis = "omnipotent";
	? wyswietl_ukosnie;
	print "\n";
	napis = "teeeeest";
	? wyswietl_ukosnie;
}
'''

s2 = '''
% test{
	print_matrix = {
		x=0;
		while x<len matrix {
			y=0;
			while y<len matrix[x] {
				print matrix[x][y];
				print "\t";
				y=y+1;
			}
			x=x+1;
			println;
		}
	};
	//matrix=[[1,2,3,4],[5,6,7,8],[9,10,11,12]];
	? print_matrix;
}
'''
node = parser.parse(s2)
#node.print_node()
eval(node)
