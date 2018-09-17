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

	def selectNext(self):
		t = None
		self.firstNumber = True
		resultInt = ''
		resultIdent = ''
		if self.position < len(self.origin) - 1: 
			self.current = self.origin[self.position]
			self.isSpace()
			t = self.isComentary()
			if self.current.isdigit():
				while self.firstNumber:
					resultInt += self.current
					if ((self.position == len(self.origin) - 1) or (self.origin[self.position + 1] == '+') or 
						(self.origin[self.position + 1] == '-') or (self.origin[self.position + 1] == '*') or
						(self.origin[self.position + 1] == '/') or (self.origin[self.position + 1] == ' ') or 
						(self.origin[self.position + 1] == ')') or (self.origin[self.position + 1] == ';')):
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
				if resultIdent != "printf":
					self.firstNumber = True
					t = Token('IDENTIFIER', resultIdent)
					self.Tkcurrent = t
					resultIdent = ''
				else:
					self.firstNumber = True
					t = Token('PRINTF', resultIdent)
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

			elif self.current == ' ':
				self.position += 1
				self.firstNumber = True

			if self.position < len(self.origin):
				self.current = self.origin[self.position]

		else:
			print("ola", self.position, len(self.origin) - 1)
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
		return ans

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

	def statment(self):
		t = self.tokens.getTokencurrent()
		if t.typo == "IDENTIFIER":
			return self.atribution() 
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
						return ans
					else:
						raise ValueError(") missing")
		elif t.typo == "BRACKETS":
			if t.value == "{":
				ans = self.statments()
				t = self.tokens.getTokencurrent()
				if t.value == "}":
					self.tokens.selectNext()
					print(self.tokens.getTokencurrent().value,self.tokens.position)
					return ans

	def atribution(self):
		t = self.tokens.getTokencurrent()
		var = t.value
		self.tokens.selectNext()
		t = self.tokens.getTokencurrent()
		if t.typo == "EQUAL":
			self.tokens.selectNext()
			return BinOp('=',[var,self.parseExpression()])
		else:
			raise("erro-Atribuiton")

class Node():
	def __init__(self):
		self.value = None
		self.children = []
	def Evaluate():
		pass

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

class BinOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self, symbolTable):
		if self.value == "=":
			return symbolTable.setValue(self.children[0],self.children[1].Evaluate(symbolTable))
		else: 
			if self.value == '+':
				return self.children[0].Evaluate(symbolTable)+self.children[1].Evaluate(symbolTable)
			elif self.value == '-':
				return self.children[0].Evaluate(symbolTable)-self.children[1].Evaluate(symbolTable)
			elif self.value == '*':
				return self.children[0].Evaluate(symbolTable)*self.children[1].Evaluate(symbolTable)
			elif self.value == '/':
				return self.children[0].Evaluate(symbolTable)//self.children[1].Evaluate(symbolTable)

class UnOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self,symbolTable):
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

class SymbolTable():
	def __init__(self):
		self.symbolTable = {}

	def getValue(self, key):
		return self.symbolTable.get(key)

	def setValue(self, key, value):
		self.symbolTable['{}'.format(key)] = value

def main():
	symbolTable = SymbolTable()
	with open("testes.c") as f:
	    content = f.readlines()
	for expression in content:
		root = Analyser(expression).statments()
		root.Evaluate(symbolTable)

if __name__ == "__main__":
	main()