class Token():
	def __init__(self, tipo, valor):
		self.tipo = tipo
		self.valor = valor

class Tokenizador():
	def __init__(self,origem):
		self.origem = origem
		self.posicao = 0
		self.atual = None

	def selecionarProximo(self):
		listaTokens = []
		firstNumber = True
		resultado = ''
		self.atual = self.origem[self.posicao]
		while self.posicao <= (len(self.origem)) - 1: 
			if self.atual.isdigit():
				while firstNumber:
					resultado += self.atual
					if ((self.posicao == len(self.origem) - 1) or (self.origem[self.posicao + 1] == '+') or 
						(self.origem[self.posicao + 1] == '-')):
							self.posicao += 1
							listaTokens.append(Token('INT', int(resultado)))
							resultado = ''
							firstNumber = False
					else:
						self.posicao += 1
						self.atual = self.origem[self.posicao]

			elif self.origem[self.posicao] == '+':
				self.posicao += 1
				firstNumber = True
				listaTokens.append(Token('PLUS', '+'))

			elif self.origem[self.posicao] == '-':
				self.posicao += 1
				firstNumber = True
				listaTokens.append(Token('MINUS', '-'))

			if self.posicao < len(self.origem):
				self.atual = self.origem[self.posicao]
		
		listaTokens.append(Token("","EOF"))
		return listaTokens

class Analisador():

	tokens = None

	def __init__(self, origem):
		self.origem = origem
		self.tokens = Tokenizador(origem)

	def analisarExpressao(self):
		op = self.tokens.selecionarProximo()

		firstNumber = True
		firstTok = True
		somar = False
		subtrair = False

		num = [0,0]
		ans = None

		for t in op:
			if firstTok:
				if t.tipo != 'INT':
					raise ValueError('Expected INT, got {}'.format(t.tipo))
				else:
					firstTok = False
			
			if (t.tipo == 'INT') and (firstNumber == True):
				num[0] += t.valor

			elif t.tipo == 'PLUS':
				if somar == True or subtrair == True :
					raise ValueError('Expected INT after math signal, got {}'.format(t.tipo))
				somar = True
				firstNumber = False

			elif t.tipo == 'MINUS':
				if subtrair == True or somar == True :
					raise ValueError('Expected INT after math signal, got {}'.format(t.tipo))
				subtrair = True
				firstNumber = False

			elif (t.tipo == 'INT') and (firstNumber == False):
				num[1] += t.valor

			if num[0] != 0 and num[1] != 0:
				if somar == True:
					num[0] = (num[0] + num[1])
					somar = False

				elif subtrair == True:
					num[0] = (num[0] - num[1])
					subtrair = False
				num[1] = 0

			if t.valor == "EOF":
				if somar == True or subtrair == True:
					raise ValueError('Find PLUS OR MINUS type at the end of expression. Not allowed')
				ans = num[0]

		return ans

if __name__ == "__main__":
	# expressoes
	with open("testes.txt") as f:
	    content = f.readlines()

	content = [x.strip().replace(" ","") for x in content]
	for expression in content: 
		print(Analisador(expression).analisarExpressao())