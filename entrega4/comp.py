class Token():
	def __init__(self, tipo, valor):
		self.tipo = tipo
		self.valor = valor

class Tokenizador():
	def __init__(self,origem):
		self.origem = origem
		self.posicao = 0
		self.atual = None
		self.Tkatual = None

	def isSpace(self):
		if self.atual == ' ':
			space = True
			while space:
				self.posicao+=1
				if self.origem[self.posicao] != ' ':
					space = False
			self.atual = self.origem[self.posicao]

	def isComentary(self):
		t = None
		if self.atual == '/':
			if self.origem[self.posicao + 1] =='*':
				comentario = True
				while comentario:
					self.posicao+=1
					if self.posicao+1 < len(self.origem):
						self.atual = self.origem[self.posicao]
						if self.atual == '*' and self.origem[self.posicao + 1] == '/':
							self.posicao+=2
							if self.posicao < len(self.origem):
								self.atual = self.origem[self.posicao]
								self.isSpace()
								comentario = False
							else:
								t = Token('','EOF')
								self.atual = ''
								self.Tkatual = Token('','EOF')
								comentario = False
					else:
						raise ValueError("Comentary not terminated.Expecting */")
		return t

	def selecionarProximo(self):
		t = None
		self.firstNumber = True
		resultado = ''
		if self.posicao <= (len(self.origem)) - 1: 
			self.atual = self.origem[self.posicao]
			self.isSpace()
			t = self.isComentary()
			if self.atual.isdigit():
				while self.firstNumber:
					resultado += self.atual
					if ((self.posicao == len(self.origem) - 1) or (self.origem[self.posicao + 1] == '+') or 
						(self.origem[self.posicao + 1] == '-') or (self.origem[self.posicao + 1] == '*') or
						(self.origem[self.posicao + 1] == '/') or (self.origem[self.posicao + 1] == ' ') or 
						(self.origem[self.posicao + 1] == ')')):
							self.posicao += 1
							t = Token('INT', int(resultado))
							self.Tkatual = Token('INT', int(resultado))
							resultado = ''
							self.firstNumber = False
					else:
						self.posicao += 1
						self.atual = self.origem[self.posicao]

			elif self.atual == '+':
				self.posicao += 1
				self.firstNumber = True
				t = Token('PLUS', '+')
				self.Tkatual = Token('PLUS', '+')

			elif self.atual == '-':
				self.posicao += 1
				self.firstNumber = True
				t = Token('MINUS', '-')
				self.Tkatual = Token('MINUS', '-')

			elif self.atual == '*':
				self.posicao += 1
				self.firstNumber = True
				t = Token('MULT', '*')
				self.Tkatual = Token('MULT', '*')

			elif self.atual == '/':
				self.posicao += 1
				self.firstNumber = True
				t = Token('DIV', '/')
				self.Tkatual = Token('DIV', '/')

			elif self.atual == '(':
				self.posicao += 1
				self.firstNumber = True
				t  = Token('PAREN','(')
				self.Tkatual = Token('PAREN','(')

			elif self.atual == ')':
				self.posicao += 1
				self.firstNumber = True
				t  = Token('PAREN',')')
				self.Tkatual = Token('PAREN',')')

			elif self.atual == ' ':
				self.posicao += 1
				self.firstNumber = True

			if self.posicao < len(self.origem):
				self.atual = self.origem[self.posicao]

		else:
			t = Token('','EOF')
			self.Tkatual = Token('','EOF')

		return t

	def getTokenAtual(self):
		return self.Tkatual

class Analisador():

	tokens = None
	def __init__(self, origem):
		self.origem = origem
		self.tokens = Tokenizador(origem)
		self.isNotEOF = True

	def fator(self):
		t = self.tokens.getTokenAtual()
		if t.tipo == "MINUS":
			self.tokens.selecionarProximo()
			return -self.fator()
		elif t.tipo == "PLUS":
			self.tokens.selecionarProximo()
			return self.fator()
		elif t.tipo == "INT":
			return t.valor
		elif t.tipo == "PAREN":
			if t.valor == "(":
				ans = self.analisarExpressao()
				t = self.tokens.getTokenAtual()	
				if t.valor == ")":
					return ans

	def term(self):
		termLoop = True
		t = self.fator()
		resposta = t
		while termLoop:
			if isinstance(t,int):
				nextT = self.tokens.selecionarProximo()
				if nextT.tipo == 'MULT':
					self.tokens.selecionarProximo()
					resposta*= self.fator()
				elif nextT.tipo == 'DIV':
					self.tokens.selecionarProximo()
					resposta/= self.fator()
				else:
					termLoop = False
		return resposta

	def analisarExpressao(self):

		self.tokens.selecionarProximo()
		retorno = self.term()
		while self.isNotEOF:
			if self.tokens.getTokenAtual().tipo == 'PLUS':
				self.tokens.selecionarProximo()
				retorno += self.term()
			elif self.tokens.getTokenAtual().tipo == 'MINUS':
				self.tokens.selecionarProximo()
				retorno -= self.term()
			elif self.tokens.getTokenAtual().valor == 'EOF' or self.tokens.getTokenAtual().valor == ')' :
				self.isNotEOF = False
		return retorno

if __name__ == "__main__":

	with open("testes.txt") as f:
	    content = f.readlines()

	for expression in content: 
		print(Analisador(expression).analisarExpressao())