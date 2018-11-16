#!/usr/bin/python
class Token():
	def __init__(self, typo, value):
		self.typo = typo
		self.value = value

class Tokenizador():
	def __init__(self,origin):
		self.origin = origin
		self.position = 0
		self.current = None
		self.Tkcurrent = None

	def isSpace(self):
		if self.current == ' ':
			space = True
			while space:
				self.position+=1
				if self.origin[self.position] != ' ':
					space = False
			self.current = self.origin[self.position]

	def isComentary(self):
		t = None
		if self.current == '/':
			if self.origin[self.position + 1] =='*':
				comentario = True
				while comentario:
					self.position+=1
					if self.position+1 < len(self.origin):
						self.current = self.origin[self.position]
						if self.current == '*' and self.origin[self.position + 1] == '/':
							self.position+=2
							if self.position < len(self.origin):
								self.current = self.origin[self.position]
								self.isSpace()
								comentario = False
							else:
								t = Token('','EOF')
								self.current = ''
								self.Tkcurrent = Token('','EOF')
								comentario = False
					else:
						raise ValueError("Comentary not terminated.Expecting */")
		return t

	def backwards(self,typo,value):
		self.position -= 1
		self.current = self.origin[self.position]
		self.Tkcurrent = Token(typo, value)

	def selectNext(self):
		t = None
		self.firstNumber = True
		resultInt = ''
		resultIdent = ''
		if self.position < len(self.origin): 
			self.current = self.origin[self.position]
			self.isSpace()
			t = self.isComentary()
			if self.current.isdigit():
				while self.firstNumber:
					resultInt += self.current
					if ((self.position == len(self.origin) - 1) or (self.origin[self.position + 1] == '+') or 
						(self.origin[self.position + 1] == '-') or (self.origin[self.position + 1] == '*') or
						(self.origin[self.position + 1] == '/') or (self.origin[self.position + 1] == ' ') or 
						(self.origin[self.position + 1] == ')') or (self.origin[self.position + 1] == ';') or
						(self.origin[self.position + 1] == '<') or (self.origin[self.position + 1] == '>')):
							self.position += 1
							t = Token('INT', int(resultInt))
							self.Tkcurrent = Token('INT', int(resultInt))
							resultInt = ''
							self.firstNumber = False
					else:
						self.position += 1
						self.current = self.origin[self.position]

			elif self.current.isalpha():
				while self.current.isalpha() or self.current.isdigit() or self.current == '_':
						resultIdent += self.current
						self.position += 1
						self.current = self.origin[self.position]
				if resultIdent == "printf":
					self.firstNumber = True
					t = Token('PRINTF', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "if":
					self.firstNumber = True
					t = Token('IF', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "else":
					self.firstNumber = True
					t = Token('ELSE', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "while":
					self.firstNumber = True
					t = Token('WHILE', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "then":
					self.firstNumber = True
					t = Token('THEN', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "scanf":
					self.firstNumber = True
					t = Token('SCANF', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "int":
					self.firstNumber = True
					t = Token('INT', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "char":
					self.firstNumber = True
					t = Token('CHAR', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "void":
					self.firstNumber = True
					t = Token('VOID', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				elif resultIdent == "return":
					self.firstNumber = True
					t = Token('RETURN', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''

				else:
					self.firstNumber = True
					t = Token('IDENTIFIER', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''

			elif self.current == ";":
				self.position += 1
				self.firstNumber = True
				t  = Token('SEMI-COLON',';')
				self.Tkcurrent = t

			elif self.current == '{':
				self.position += 1
				self.firstNumber = True
				t  = Token('BRACKETS','{')
				self.Tkcurrent = t

			elif self.current == '}':
				self.position += 1
				self.firstNumber = True
				t  = Token('BRACKETS','}')
				self.Tkcurrent = t

			elif self.current == '+':
				self.position += 1
				self.firstNumber = True
				t  = Token('PLUS','+')
				self.Tkcurrent = t

			elif self.current == '=':
				self.position += 1
				self.current = self.origin[self.position]
				if self.current == '=':
					self.position += 1
					self.firstNumber = True
					t  = Token('RELATIONAL','==')
					self.Tkcurrent = Token('RELATIONAL','==')
				else:
					self.firstNumber = True
					t  = Token('EQUAL','=')
					self.Tkcurrent = t

			elif self.current == '-':
				self.position += 1
				self.firstNumber = True
				t = Token('MINUS', '-')
				self.Tkcurrent = Token('MINUS', '-')

			elif self.current == '*':
				self.position += 1
				self.firstNumber = True
				t = Token('MULT', '*')
				self.Tkcurrent = Token('MULT', '*')

			elif self.current == '/':
				self.position += 1
				self.firstNumber = True
				t = Token('DIV', '/')
				self.Tkcurrent = Token('DIV', '/')

			elif self.current == '(':
				self.position += 1
				self.firstNumber = True
				t  = Token('PAREN','(')
				self.Tkcurrent = Token('PAREN','(')

			elif self.current == ')':
				self.position += 1
				self.firstNumber = True
				t  = Token('PAREN',')')
				self.Tkcurrent = Token('PAREN',')')

			elif self.current == '|':
				self.position += 1
				self.current = self.origin[self.position]
				if self.current == '|':
					self.position += 1
					self.firstNumber = True
					t  = Token('OR','||')
					self.Tkcurrent = Token('OR','||')

			elif self.current == '&':
				self.position += 1
				self.current = self.origin[self.position]
				if self.current == '&':
					self.position += 1
					self.firstNumber = True
					t  = Token('AND','&&')
					self.Tkcurrent = Token('AND','&&')

			elif self.current == '>':
				self.position += 1
				self.firstNumber = True
				t  = Token('RELATIONAL','>')
				self.Tkcurrent = Token('RELATIONAL','>')

			elif self.current == '<':
				self.position += 1
				self.firstNumber = True
				t  = Token('RELATIONAL','<')
				self.Tkcurrent = Token('RELATIONAL','<')

			elif self.current == '!':
				self.position += 1
				self.firstNumber = True
				t  = Token('NOT','!')
				self.Tkcurrent = Token('NOT','!')

			elif self.current == ',':
				self.position += 1
				self.firstNumber = True
				t  = Token('COMMA',',')
				self.Tkcurrent = Token('COMMA',',')

			elif self.current == ' ':
				self.position += 1
				self.firstNumber = True
				
			if self.position < len(self.origin):
				self.current = self.origin[self.position]

		else:
			t = Token('','EOF')
			self.Tkcurrent = Token('','EOF')
			
		return t

	def getTokencurrent(self):
		return self.Tkcurrent

class Analyser():

	tokens = None
	def __init__(self, origin):
		self.origin = origin
		self.tokens = Tokenizador(origin)
		self.tokens.selectNext()
		self.isNotEOF = True

	def factor(self):
		t = self.tokens.getTokencurrent()

		if t.typo == "MINUS":
			self.tokens.selectNext()
			return UnOp('-',[self.factor()])
		elif t.typo == "PLUS":
			self.tokens.selectNext()
			return UnOp('+',[self.factor()])
		elif t.typo == "INT":
			v = t.value
			self.tokens.selectNext()
			return IntVal(v)
		elif t.typo == "PAREN":
			if t.value == "(":
				self.tokens.selectNext()
				ans = self.parseExpression()
				t = self.tokens.getTokencurrent()	
				if t.value == ")":
					self.tokens.selectNext()
				else:
					raise ValueError(") missing")
				return ans
			else:
				raise ValueError("erro parenteses factor")
		elif t.typo == "IDENTIFIER":
			v = t.value
			self.tokens.selectNext()
			return VarVal(v)
		else:
			raise ValueError("Factor error")

	def term(self):
		ans = self.factor()
		while self.tokens.getTokencurrent().typo == 'MULT' or self.tokens.getTokencurrent().typo == 'DIV':
			if self.tokens.getTokencurrent().typo == 'MULT':
				self.tokens.selectNext()
				ans = BinOp('*',[ans,self.factor()])
			elif self.tokens.getTokencurrent().typo == 'DIV':
				self.tokens.selectNext()
				ans = BinOp('/',[ans,self.factor()])
			else:
				raise ValueError("erro term")
		return ans

	def parseExpression(self):
		ans = self.term()
		while self.tokens.getTokencurrent().typo == 'PLUS' or self.tokens.getTokencurrent().typo == 'MINUS':
			if self.tokens.getTokencurrent().typo == 'PLUS':
				self.tokens.selectNext()
				ans = BinOp('+',[ans,self.term()])
			elif self.tokens.getTokencurrent().typo == 'MINUS':
				self.tokens.selectNext()
				ans = BinOp('-',[ans,self.term()])
			else:
				raise ValueError("erro parseExpression")
		return ans

	def relExpression(self):		
		ans = self.parseExpression()
		t = self.tokens.getTokencurrent()
		if t.typo == "RELATIONAL":
			if t.value == ">": #bigger than
				self.tokens.selectNext()
				return BinOp('>',[ans,self.parseExpression()])
			elif t.value == "<": #less than
				self.tokens.selectNext()
				return BinOp('<',[ans,self.parseExpression()])
			elif t.value == "==": #double equal
				self.tokens.selectNext()
				return BinOp('==',[ans,self.parseExpression()])
		else:
			raise ValueError("relExpresion error")

	def boolFactor(self):
		t = self.tokens.getTokencurrent()	
		if t.typo == "NOT":
			self.tokens.selectNext()
			return UnOp('!',[self.boolFactor()])
		else:
			return self.relExpression() 

	def boolTerm(self):
		ans = self.boolFactor()
		while self.tokens.getTokencurrent().typo == 'AND':
			self.tokens.selectNext()
			ans = BinOp('&&',[ans,self.boolFactor()])

		return ans

	def boolExpression(self):
		ans = self.boolTerm()
		while self.tokens.getTokencurrent().typo == 'OR':
			self.tokens.selectNext()
			ans = BinOp('||',[ans,self.boolTerm()])

		return ans

	def typeRecognize(self):
		t = self.tokens.getTokencurrent()
		if t.typo == "VOID" or t.typo == "INT" or t.typo == "CHAR":	
			return True
		return False
	"""
	def mainEvaluate(self):
		t = self.tokens.getTokencurrent()

		if self.typeRecognize():
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo == "MAIN":
				self.tokens.selectNext()
				t = self.tokens.getTokencurrent()
				if t.typo == "PAREN":
					if t.value == "(":
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						if t.typo == "PAREN":
							if t.value == ")":
								self.tokens.selectNext()
								return self.statments()
				else:
					raise ValueError("mainParen Error")
			else:
				raise ValueError("main needed")
		else:
			raise ValueError("typo missing")
	"""
	def funcStatments(self):
		t = self.tokens.getTokencurrent()
		childrens = []
		while t.typo != None:
			if self.typeRecognize():
				funcDecList = []
				t = self.tokens.getTokencurrent()
				typo_temp = t.typo
				funcDecList.append(typo_temp)
				self.tokens.selectNext()
				t = self.tokens.getTokencurrent()
				typo = t.typo
				value = t.value
				self.tokens.selectNext()
				t = self.tokens.getTokencurrent()
				if t.typo == "PAREN": 	
					self.tokens.backwards(typo,value)
					t = self.tokens.getTokencurrent()
					funcName = t.value
					self.tokens.selectNext()
					self.tokens.selectNext()
					while True:
						if self.typeRecognize():
							t = self.tokens.getTokencurrent()
							typo_temp = t.typo
							self.tokens.selectNext()
							t = self.tokens.getTokencurrent()
							value = t.value
							funcDecList.append(VarDecNode(typo_temp,[value]))
							self.tokens.selectNext()
							t = self.tokens.getTokencurrent()
							if t.typo == "COMMA":
								self.tokens.selectNext()
								continue
							else:
								break
						else:
							break
					self.tokens.selectNext()
					commandsStuff = self.statments()
					funcDecList.append(commandsStuff)
					childrens.append(funcDec(funcName,funcDecList))
					self.tokens.selectNext()
					t = self.tokens.getTokencurrent()
			else:
				t.typo = None

		mainCall = funcCall('main',[])
		childrens.append(mainCall)
		master = masterNode(childrens)
		return master

	def statments(self):

		t = self.tokens.getTokencurrent()
		if t.typo == "BRACKETS":
			if t.value == "{":
				statments = []
				self.tokens.selectNext()
				while t.value != "}":
					s = self.statment()
					t = self.tokens.getTokencurrent()
					if t.typo == "SEMI-COLON":
						statments.append(s)
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
				return StatmentsNode(statments)
			else:
				raise ValueError("erro brackets statments")

	def statment(self):
		varDecList = []
		t = self.tokens.getTokencurrent()
		if t.typo == "IDENTIFIER":
			return self.atribution()

		elif self.typeRecognize():
			typo_temp = t.typo
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			typo = t.typo
			value = t.value
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo != "PAREN":
				t = self.tokens.getTokencurrent()
				self.tokens.backwards(typo,value)
				t = self.tokens.getTokencurrent()
				varDecList.append(t.value)
				while t.typo != "SEMI-COLON":
					self.tokens.selectNext()
					t = self.tokens.getTokencurrent()
					if t.typo == "COMMA":
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						varDecList.append(t.value)
				return VarDecNode(typo_temp,varDecList)
		elif t.typo == "PRINTF":
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo == "PAREN":
				if t.value == "(":
					self.tokens.selectNext()
					ans = PrintfNode([self.parseExpression()])
					t = self.tokens.getTokencurrent()	
					if t.value == ")":
						self.tokens.selectNext()
						if self.tokens.getTokencurrent().typo != "SEMI-COLON":
							raise ValueError("error printf paren")
						return ans
					else:
						raise ValueError(") missing")
				else:
					raise ValueError("statment paren error")
		elif t.typo == "IF":
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo == "PAREN":
				if t.value == "(":
					self.tokens.selectNext()
					condition = self.boolExpression()
					t = self.tokens.getTokencurrent()	
					if t.value == ")":
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						if t.typo == "THEN":
							self.tokens.selectNext()
							trueState = self.statment()
							t = self.tokens.getTokencurrent()
							if t.typo == "ELSE":
								self.tokens.selectNext()
								falseState = self.statment()
							else:
								falseState = None

					else:
						raise ValueError(") missing")

			return IfElseNode([condition,trueState,falseState])

		elif t.typo == "WHILE":
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo == "PAREN":
				if t.value == "(":
					self.tokens.selectNext()
					condition = self.boolExpression()
					t = self.tokens.getTokencurrent()	
					if t.value == ")":
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						if t.typo == "THEN":
							self.tokens.selectNext()
							trueState = self.statment()
					else:
						raise ValueError(") missing")

			return WhileNode([condition,trueState])

		elif t.typo == "RETURN":
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			r = returnNode([self.parseExpression()])
			return r

		elif t.typo == "BRACKETS":
			if t.value == "{":
				ans = self.statments()
				t = self.tokens.getTokencurrent()
				if t.value == "}":
					self.tokens.selectNext()
					return ans
				else:
					raise ValueError("Erro brackets comando")

	def atribution(self):
		t = self.tokens.getTokencurrent()
		var = t.value
		self.tokens.selectNext()
		t = self.tokens.getTokencurrent()
		if t.typo == "EQUAL":
			self.tokens.selectNext()
			t = self.tokens.getTokencurrent()
			if t.typo == "SCANF":
				self.tokens.selectNext()
				t = self.tokens.getTokencurrent()
				if t.typo == "PAREN":
					if t.value == "(":
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						if t.value == ")":
							self.tokens.selectNext()
							ans = ScanfNode()
							return BinOp('=',[var,ans])						
						else:
							raise ValueError("erro parentes scanf")
			elif t.typo == "IDENTIFIER":
				funcName = t.value
				typo = t.typo
				value = t.value
				self.tokens.selectNext()
				t = self.tokens.getTokencurrent()

				if t.typo == "PAREN":
					if t.value == "(":
						args  = []
						self.tokens.selectNext()
						while t.value != ")":	
							ans = self.parseExpression()
							args.append(ans)
							t = self.tokens.getTokencurrent()
							if t.typo == "COMMA":
								self.tokens.selectNext()
								t = self.tokens.getTokencurrent()
						
						self.tokens.selectNext()
						t = self.tokens.getTokencurrent()
						if t.typo == "SEMI-COLON":
							return BinOp('=',[var,funcCall(funcName,args)])
				else:
					self.tokens.backwards(typo,value)
					t = self.tokens.getTokencurrent()
					return BinOp('=',[var,self.parseExpression()])
			else:
				return BinOp('=',[var,self.parseExpression()])
		else:
			raise ValueError("erro-Atribuiton")

class Node():
	def __init__(self):
		self.value = None
		self.children = []
	def Evaluate():
		pass

class masterNode(Node):
	def __init__(self,children):
		self.children = children

	def Evaluate(self):
		symbolTable = SymbolTable()
		for i in self.children:
			i.Evaluate(symbolTable)

class returnNode(Node):
	def __init__(self, children):
		self.children = children

	def Evaluate(self,symbolTable):
		ans = self.children[0].Evaluate(symbolTable)
		return ans

class funcDec(Node):
	def __init__(self,value,children):
		self.value = value
		self.children = children
		
	def Evaluate(self,symbolTable):
		symbolTable.createValue('func',self.value)
		symbolTable.setValue(self.value,self)

class funcCall(Node):
	def __init__(self,value,children):
		self.value = value
		self.children = children
		self.NewSymbolTable = SymbolTable() #Passar a symboltable atual como ancestor

	def Evaluate(self,symbolTable):
		self.NewSymbolTable.ancestor = symbolTable

		func = symbolTable.getValue(self.value)
		argsName = []
		for i in range(1, len(func.children)-1):
			ref = func.children[i].children[0]
			argsName.append(ref) #precisa guardar o nome da variável aqui
			func.children[i].Evaluate(self.NewSymbolTable) #Declarou os argumentos na nova ST

		if (len(self.children) != 0):
			for i, j in enumerate(self.children):
				self.NewSymbolTable.setValue(argsName[i], j.Evaluate(symbolTable)) #passar o valor dos filhos para a nova ST na ordem correta

        #Evaluate do ultimo filho (comandos)
		for e in func.children[len(func.children)-1].children:
			tp = type(e) #aquiii
			typo = "<class '__main__.returnNode'>"
			if str(tp)  == typo:
				return e.Evaluate(self.NewSymbolTable)
			else:
				e.Evaluate(self.NewSymbolTable)

class StatmentsNode(Node):
	def __init__(self, children):
		self.children = children

	def Evaluate(self,symbolTable):
		for i in self.children:
			i.Evaluate(symbolTable)

class PrintfNode(Node):
	def __init__(self, children):
		self.children = children

	def Evaluate(self,symbolTable):
		print(self.children[0].Evaluate(symbolTable))

class IfElseNode(Node):
	def __init__(self, children):
		self.children = children

	def Evaluate(self,symbolTable):

		if self.children[0].Evaluate(symbolTable):
			return self.children[1].Evaluate(symbolTable)
		elif self.children[2] != None:
			return self.children[2].Evaluate(symbolTable)

class WhileNode(Node):
	def __init__(self, children):
		self.children = children

	def Evaluate(self,symbolTable):
		while self.children[0].Evaluate(symbolTable):
			self.children[1].Evaluate(symbolTable)

class ScanfNode(Node):
	def Evaluate(self,symbolTable):
		value = int(input("Choose a number: "))
		return value 

class BinOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self, symbolTable):
		if self.value == "=":
			symbolTable.setValue(self.children[0],self.children[1].Evaluate(symbolTable))
		else: 
			if self.value == '+':
				return self.children[0].Evaluate(symbolTable)+self.children[1].Evaluate(symbolTable)
			elif self.value == '-':
				return self.children[0].Evaluate(symbolTable)-self.children[1].Evaluate(symbolTable)
			elif self.value == '*':
				return self.children[0].Evaluate(symbolTable)*self.children[1].Evaluate(symbolTable)
			elif self.value == '/':
				return self.children[0].Evaluate(symbolTable)//self.children[1].Evaluate(symbolTable)
			elif self.value == '>':
				return self.children[0].Evaluate(symbolTable)>self.children[1].Evaluate(symbolTable)
			elif self.value == '<':
				return self.children[0].Evaluate(symbolTable)<self.children[1].Evaluate(symbolTable)
			elif self.value == '==':
				return self.children[0].Evaluate(symbolTable)==self.children[1].Evaluate(symbolTable)
			elif self.value == '&&':
				return self.children[0].Evaluate(symbolTable) and self.children[1].Evaluate(symbolTable)
			elif self.value == '||':
				return self.children[0].Evaluate(symbolTable) or self.children[1].Evaluate(symbolTable)

class UnOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self,symbolTable):
		if self.value == '!':
			return not self.children[0].Evaluate(symbolTable)
		if self.value == '+':
			return self.children[0].Evaluate(symbolTable)
		else:
			return -self.children[0].Evaluate(symbolTable)

class IntVal(Node):
	def __init__(self, value):
		self.value = value

	def Evaluate(self,symbolTable):
		return self.value

class VarVal(Node):
	def __init__(self, value):
		self.value = value

	def Evaluate(self,symbolTable):
		return symbolTable.getValue(self.value)

class NoOp(Node):
	def __init__(self):
		self.value = None

	def Evaluate(self,symbolTable):
		return self.value

class VarDecNode(Node):
	def __init__(self,value,children):
		self.children = children
		self.value = value

	def Evaluate(self,symbolTable):
		for i in self.children:
			symbolTable.createValue(self.value,i)

class SymbolTable():
	def __init__(self):
		self.symbolTable = {}
		self.ancestor = None 

	def getValue(self, key):
		if key in self.symbolTable:
			return self.symbolTable.get(key)[1]
		else:
			if self.ancestor:
				return self.ancestor.getValue(key)
			else:
				raise ValueError("Senpai")

	def setValue(self, key, value):
		if key in self.symbolTable:
			keyType = self.symbolTable.get(key)[0].lower()
			valueType = value
			if "<class '{}'>".format(keyType) == str(type(valueType)) or keyType == 'func':
				self.symbolTable[key][1] = value
			else:
				raise ValueError("wrong type for variable")
		else:
			raise ValueError("setValue error")

	def createValue(self,typo,key):
		self.symbolTable['{}'.format(key)] = [typo,None]


def main():

	with open("testes.c") as f:
		content = f.readlines()
	content = [x.strip() for x in content] 

	code = ""
	for line in content:
		code+=line

	root = Analyser(code).funcStatments()
	root.Evaluate()

if __name__ == "__main__":
	main()