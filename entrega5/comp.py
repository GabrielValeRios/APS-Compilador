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
		result = ''
		if self.position <= (len(self.origin)) - 1: 
			self.current = self.origin[self.position]
			self.isSpace()
			t = self.isComentary()
			if self.current.isdigit():
				while self.firstNumber:
					result += self.current
					if ((self.position == len(self.origin) - 1) or (self.origin[self.position + 1] == '+') or 
						(self.origin[self.position + 1] == '-') or (self.origin[self.position + 1] == '*') or
						(self.origin[self.position + 1] == '/') or (self.origin[self.position + 1] == ' ') or 
						(self.origin[self.position + 1] == ')')):
							self.position += 1
							t = Token('INT', int(result))
							self.Tkcurrent = Token('INT', int(result))
							result = ''
							self.firstNumber = False
					else:
						self.position += 1
						self.current = self.origin[self.position]

			elif self.current == '+':
				self.position += 1
				self.firstNumber = True
				t = Token('PLUS', '+')
				self.Tkcurrent = Token('PLUS', '+')

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
					pass #raise
				return ans

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

class Node():
	def __init__(self):
		self.value = None
		self.children = []
	def Evaluate():
		pass

class BinOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self):
		if self.value == '+':
			return self.children[0].Evaluate()+self.children[1].Evaluate()
		elif self.value == '-':
			return self.children[0].Evaluate()-self.children[1].Evaluate()
		elif self.value == '*':
			return self.children[0].Evaluate()*self.children[1].Evaluate()
		elif self.value == '/':
			return self.children[0].Evaluate()//self.children[1].Evaluate()

class UnOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self):
		if self.value == '+':
			return self.children[0].Evaluate()
		else:
			return -self.children[0].Evaluate()

class IntVal(Node):
	def __init__(self, value):
		self.value = value

	def Evaluate(self):
		return self.value

class NoOp(Node):
	def __init__(self):
		self.value = None

	def Evaluate(self):
		return self.value

def main():
	with open("testes.c") as f:
	    content = f.readlines()
	for expression in content: 
		root = Analyser(expression).parseExpression()
		print(root.Evaluate())

if __name__ == "__main__":
	main()