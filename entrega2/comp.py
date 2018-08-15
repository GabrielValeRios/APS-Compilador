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
		flagDigit = True
		resultado = ''
		self.atual = self.origem[self.posicao]
		while self.posicao <= (len(self.origem)) - 1: 
			if self.atual.isdigit():
				while flagDigit:
					resultado += self.atual
					if ((self.posicao == len(self.origem) - 1) or (self.origem[self.posicao + 1] == '+') or 
						(self.origem[self.posicao + 1] == '-')):
							self.posicao += 1
							listaTokens.append(Token('INT', int(resultado)))
							resultado = ''
							flagDigit = False
					else:
						self.posicao += 1
						self.atual = self.origem[self.posicao]

			elif self.origem[self.posicao] == '+':
				self.posicao += 1
				flagDigit = True
				listaTokens.append(Token('PLUS', '+'))

			elif self.origem[self.posicao] == '-':
				self.posicao += 1
				flagDigit = True
				listaTokens.append(Token('MINUS', '-'))

			if self.posicao < len(self.origem):
				self.atual = self.origem[self.posicao]
			
		return listaTokens

class Analisador():

	tokens = None

	def __init__(self, origem):
		self.origem = origem
		self.tokens = Tokenizador(origem)

	def analisarExpressao(self):
		op = self.tokens.selecionarProximo()
		flagDigit = True
		somar = False
		subtrair = False
		num = [0,0]
		resposta = []

		for t in op:
			if (t.tipo == 'INT') and (flagDigit == True):
				num[0] += t.valor

			elif t.tipo == 'PLUS':
				somar = True
				flagDigit = False

			elif t.tipo == 'MINUS':
				subtrair = True
				flagDigit = False

			elif (t.tipo == 'INT') and (flagDigit == False):
				num[1] += t.valor

			if num[0] != 0 and num[1] != 0:
				if somar == True:
					num[0] = (num[0] + num[1])
					somar = False

				elif subtrair == True:
					num[0] = (num[0] - num[1])
					subtrair = False
				num[1] = 0

		return [num[0],op]

if __name__ == "__main__":

	tokObjsList = []
	# expressoes
	with open("testes.txt") as f:
	    content = f.readlines()

	content = [x.strip().replace(" ","") for x in content]
	for expression in content: 
		alsObj = Analisador(expression).analisarExpressao()
		for tok in alsObj[1]:
			tokObjsList.append(tok)
		print(alsObj[0])

	tokObjsList.append(Token("","EOF"))
