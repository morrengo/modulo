import parser
import sys

class Scope:
	def __init__(self,name,scope = None):
		self.name = name
		if scope:
			self.scope=scope
		else:
			self.scope = {}
	def add_to_scope(self,definition,val):
		self.scope[definition]=val
	def get_from_scope(self,definition):
		try:
			return self.scope[definition]
		except:
			return None
	
curr_scope = Scope('main')
scopes = []

def push_scope():
	global curr_scope,scopes
	scopes.append(curr_scope)
	curr_scope = Scope('test',dict(curr_scope.scope))

def add_to_scope(definition,val):
	curr_scope.add_to_scope(definition,val)

def pop_scope():
	global curr_scope
	curr_scope = scopes.pop()

def get_from_scope(definition):
	try:
		return curr_scope.get_from_scope(definition)
	except:
		return None

def eval(node):
	global curr_scope
	try:
		if(node.node_type == 'module'):
			push_scope()
			curr_scope = Scope(node.info)
			eval(node.children[0])
			res = dict(curr_scope.scope)
			pop_scope()
			return res
		elif(node.node_type == 'return'):
			return eval(node.children[0])
		elif(node.node_type == 'body'):
			for child in node.children:
				res = eval(child)
				if(res is not None):
					return res
		elif(node.node_type == "assign"):
			target = node.children[0]
			expression = node.children[1]
			val = eval(expression)
			if(target.node_type == 'inner'):
				target.node_type = 'inner_assign'
				target = eval(target)
				target[0].add_to_scope(target[1],val)
				return
			add_to_scope(target.info,val)
		elif(node.node_type == "assign_proc"):
			target = node.children[0]
			expression = node.children[1]
			if(target.node_type == 'inner'):
				target.node_type = 'inner_assign'
				target = eval(target)
				target[0].add_to_scope(target[1],expression)
				return
			add_to_scope(target.info, expression)
		elif(node.node_type == 'args'):
			for child in node.children:
				eval(child)
			#for child in node.children
		elif(node.node_type == "assign_mod"):
			target = node.children[0]
			mod = node.children[1]
			if(target.node_type == 'inner'):
				target.node_type = 'inner_assign'
				target = eval(target)
				target[0].add_to_scope(target[1],Scope('test',eval(mod)))
				return
			add_to_scope(target.info, Scope(target.info,eval(mod)))
		elif(node.node_type == "procedure"):
			if(node.children[0].node_type == 'inner'):
				node.children[0].node_type = 'inner_assign'
				res =  eval(node.children[0])
				scope = res[0]
				node.children[0].node_type = 'inner'
				push_scope()
				curr_scope = scope
				ret = eval(get_from_scope(res[1]))
				pop_scope()
				return ret
			elif(isinstance(get_from_scope(node.children[0].info),parser.Node)):
				fun = get_from_scope(node.children[0].info)
				if len(node.children)==2 :
					push_scope()
					eval(node.children[1])
					ret = eval(fun)
					pop_scope()
					return ret
				return eval(fun)
			else:
				raise Exception("\'"+node.node_type+"\' is not a function or is undefined")
		elif(node.node_type == 'println'):
			if node.children is None or len(node.children)==0:
				print
			else:
				print eval(node.children[0])
		elif(node.node_type == 'print'):
			sys.stdout.write(str(eval(node.children[0])))
		elif(node.node_type == 'while'):
			while eval(node.children[0])==True :
				res = eval(node.children[1])
				if(res is not None):
					return res

		elif(node.node_type == 'if'):
			if( eval(node.children[0]) == True):
				ret = eval(node.children[1])
				if(ret is not None):
					return ret
				return
			if(len(node.children) > 2):
				for child in node.children[2:]:
					if(child.node_type == 'else'):
						ret = eval(child.children[0])
						if(ret is not None):
							return ret
						return
					if(eval(child.children[0]) == True):
						ret = eval(child.children[1])
						if(ret is not None):
							return ret
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

		elif(node.node_type == 'inner'):
			val = get_from_scope(node.children[0].info)
			try:
				if(node.children[1].node_type == 'id'):
					val = val.get_from_scope(node.children[1].info)
				else:
					push_scope()
					curr_scope = val
					val = eval(node.children[1])
					pop_scope()
			except:
				raise Exception("variable doesn't have inner scope")
				return
			if val is not None:
				return val
			else:
				raise Exception("undefined variable \'"+node.info+"\'")

		elif(node.node_type == 'inner_assign'):
			val = get_from_scope(node.children[0].info)
			try:
				if(node.children[1].node_type != 'id'):
					node.children[1].node_type = 'inner_assign'
					push_scope()
					curr_scope = val
					ret_scope = val
					val = eval(node.children[1])
					pop_scope()
				else:
					return [val,node.children[1].info]
			except:
				raise Exception("variable doesn't have inner scope")
				return
			if val is not None:
				return val
			else:
				raise Exception("undefined variable \'"+node.info+"\'")

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
% {
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
% {
	matrix_mod = %{
		matrix = [];
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
	};
	matrix_mod.matrix =
		[[1,2 ,3 ,4 ],
		 [5,6 ,7 ,8 ],
		 [9,10,11,12]];
	? matrix_mod.print_matrix;
}
'''

s3 = '''
%{
  a=10;
  f={
    println a;
  	if(a<=1){
  	  !a;
  	} else {
      !a * ?f(a=a-1);
  	}
  };
  println ?f(a=7);
  println a;
}
'''
s4='''
% {
	var1 = 10;
	mod1 = %{
		mod2 = %{
			map2elem={
				?asd;
				println res;
			};
		};
	};
	mod1.mod2.asd ={
		res=1234;
	};
	?mod1.mod2.map2elem;
}'''

s5='''
% {
	Math = %{
		fibo_arg = 10;
		fibo = {
			if fibo_arg <= 1{
				!fibo_arg;
			} else {
				!?fibo(fibo_arg = fibo_arg - 1)+
				 ?fibo(fibo_arg = fibo_arg - 2);
			}
		};
	};
	println ?Math.fibo;

	Math.fact_arg =10;
	Math.fact ={
		if fact_arg <= 1{
			!fact_arg;
		} else {
			!fact_arg * ?fact(fact_arg = fact_arg-1);
		}	
	};
	println ?Math.fact;
	println ?Math.fact;
}
'''

node = parser.parse(s5)
#node.print_node()
eval(node)