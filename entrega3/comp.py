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
						(self.origem[self.posicao + 1] == '/') or (self.origem[self.posicao + 1] == ' ')):
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

	def term(self):
		termLoop = True
		resposta = None
		while termLoop:
			t = self.tokens.getTokenAtual()
			if (t.tipo == 'INT'):
				if resposta == None:
					retorno = t.valor
				else:
					retorno = resposta
				nextT = self.tokens.selecionarProximo()
				if nextT.tipo == 'MULT':
					nextT = self.tokens.selecionarProximo()
					if nextT.tipo == 'INT':
						retorno *= nextT.valor
						resposta = retorno
					else:
						raise ValueError("Expected INT, got {} instead".format(nextT.valor))
				elif nextT.tipo == 'DIV':
					nextT = self.tokens.selecionarProximo()
					if nextT.tipo == 'INT':
						retorno //= nextT.valor
						resposta = retorno
					else:
						raise ValueError("Expected INT, got {} instead".format(nextT.valor))
				elif nextT.tipo == 'INT':
					raise ValueError("Expected OPERATION, got {} instead".format(nextT.valor))
				else:
					termLoop = False
			elif (t.valor == 'EOF'):
				raise EOFError("Empty file")
			else:
				raise ValueError("Expected INT, got {} instead".format(t.valor))

		return retorno

	def analisarExpressao(self):

		self.tokens.selecionarProximo()
		retorno = self.term()
		while self.isNotEOF:
			if self.tokens.getTokenAtual().tipo == 'PLUS':
				nextT = self.tokens.selecionarProximo()
				if nextT.tipo == 'INT':
					retorno += self.term()
				else:
					raise ValueError("Expected INT, got {} instead".format(nextT.valor))
			elif self.tokens.getTokenAtual().tipo == 'MINUS':
				nextT = self.tokens.selecionarProximo()
				if nextT.tipo == 'INT':
					retorno -= self.term()
				else:
					raise ValueError("Expected INT, got {} instead".format(nextT.valor))
			elif self.tokens.getTokenAtual().valor == 'EOF':
				self.isNotEOF = False
			else:
				self.term()

		return retorno

if __name__ == "__main__":

	with open("testes.txt") as f:
	    content = f.readlines()

	for expression in content: 
		print(Analisador(expression).analisarExpressao())