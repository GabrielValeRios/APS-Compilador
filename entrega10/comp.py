var = []
Asscode = []

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
			else:
				return BinOp('=',[var,self.parseExpression()])
		else:
			raise ValueError("erro-Atribuiton")

class Node():
	def __init__(self):
		self.value = None
		self.children = []
		self.id = None
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
		var = self.children[0].Evaluate(symbolTable)
		Asscode.append("MOV EBX, [{}]".format(var))
		Asscode.append("PUSH EBX")
		Asscode.append("CALL print")
		#print(self.children[0].Evaluate(symbolTable))

class IfElseNode(Node):
	def __init__(self, children):
		self.children = children
		self.id = None

	def Evaluate(self,symbolTable):
		self.id = Id.getNew("loop")
		symbolTable.setValue('loop', self.id)
		Asscode.append("LOOP_" + "{}".format(self.id))
		self.children[0].Evaluate(symbolTable)
		self.children[1].Evaluate(symbolTable)
		Asscode.append("JUMP LOOP_" + "{}".format(self.id))
		Asscode.append("EXIT_" + "{}".format(self.id))

		if self.children[2] != None:
			self.id = Id.getNew("loop")
			symbolTable.setValue('loop', self.id)
			Asscode.append("LOOP_" + "{}".format(self.id))
			self.children[2].Evaluate(symbolTable)
			Asscode.append("JUMP LOOP_" + "{}".format(self.id))
			Asscode.append("EXIT_" + "{}".format(self.id))

class WhileNode(Node):
	def __init__(self, children):
		self.children = children
		self.id = None

	def Evaluate(self,symbolTable):
		self.id = Id.getNew("loop")
		symbolTable.setValue('loop', self.id)
		Asscode.append("LOOP_" + "{}".format(self.id))
		#while self.children[0].Evaluate(symbolTable):
		self.children[0].Evaluate(symbolTable)
		self.children[1].Evaluate(symbolTable)
		Asscode.append("JUMP LOOP_" + "{}".format(self.id))
		Asscode.append("EXIT_" + "{}".format(self.id))

class ScanfNode(Node):
	def Evaluate(self,symbolTable):
		value = int(input("Choose a number"))
		return value 

class BinOp(Node):
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate(self, symbolTable):
		if self.value == "=":
			key = str(self.children[0]) + "_" + str(symbolTable.id)
			if key not in var: 
				var.append(key)
			self.children[1].Evaluate(symbolTable)
			Asscode.append("MOV [{}], EBX".format(key))
			#symbolTable.setValue(key,self.children[1].Evaluate(symbolTable))

		else: 
			if self.value == '+':
				test = self.children[0].Evaluate(symbolTable)
				if test != None:
					Asscode.append("MOV EBX, {}".format(test))
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("ADD EBX, EAX")
				#return self.children[0].Evaluate(symbolTable)+self.children[1].Evaluate(symbolTable)
			elif self.value == '-':
				self.children[0].Evaluate(symbolTable)
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("SUB EBX, EAX")
				#return self.children[0].Evaluate(symbolTable)-self.children[1].Evaluate(symbolTable)
			elif self.value == '*':
				self.children[0].Evaluate(symbolTable)
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("IMUL EBX, EAX")
				#return self.children[0].Evaluate(symbolTable)*self.children[1].Evaluate(symbolTable)
			elif self.value == '/':
				self.children[0].Evaluate(symbolTable)
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("IDIV EBX, EAX")
				#return self.children[0].Evaluate(symbolTable)//self.children[1].Evaluate(symbolTable)

			elif self.value == '>':
				self.children[0].Evaluate(symbolTable)
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("CMP EAX, EBX")
				Asscode.append("CALL binop_jg")
				Asscode.append("CMP EBX, False")
				Asscode.append("JE EXIT_{}".format(symbolTable.getValue('loop')))
				#return self.children[0].Evaluate(symbolTable)>self.children[1].Evaluate(symbolTable)
			elif self.value == '<':
				self.children[0].Evaluate(symbolTable)
				Asscode.append("MOV EAX,{}".format(self.children[1].value))
				Asscode.append("CMP EAX, EBX")
				Asscode.append("CALL binop_jl")
				Asscode.append("CMP EBX, False")
				Asscode.append("JE EXIT_{}".format(symbolTable.getValue('loop')))
				#return self.children[0].Evaluate(symbolTable)<self.children[1].Evaluate(symbolTable)

			"""
			elif self.value == '==':
				return self.children[0].Evaluate(symbolTable)==self.children[1].Evaluate(symbolTable)
			elif self.value == '&&':
				return self.children[0].Evaluate(symbolTable) and self.children[1].Evaluate(symbolTable)
			elif self.value == '||':
				return self.children[0].Evaluate(symbolTable) or self.children[1].Evaluate(symbolTable)
			"""

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
		Asscode.append("MOV EBX," + str(self.value))
		#return self.value

class VarVal(Node):
	def __init__(self, value):
		self.value = value

	def Evaluate(self,symbolTable):
		return str(self.value) + "_" + str(symbolTable.id)
		#return symbolTable.getValue(self.value)

class NoOp(Node):
	def __init__(self):
		self.value = None

	def Evaluate(self,symbolTable):
		return self.value

class SymbolTable():
	def __init__(self):
		self.symbolTable = {}
		self.id = None

	def getValue(self, key):
		return self.symbolTable.get(key)

	def setValue(self, key, value):
		self.symbolTable[key] = value

class Id():

	id_gen = {}

	@staticmethod
	def getNew(name):
		if name in Id.id_gen:
			Id.id_gen[name] += 1
			return Id.id_gen[name]
		else:
			Id.id_gen[name] = 0
			return Id.id_gen[name]

class AssemblyCode():
	def __init__(self, var, code):
		self.var = var
		self.code = code

	def Buildfile(self):
		first = ['SYS_EXIT equ 1',
				 'SYS_READ equ 3',
				 'SYS_WRITE equ 4',
				 'STDIN equ 0',
				 'STDOUT equ 1',
				 'True equ 1',
				 'False equ 0',
				 'segment . data',
				 'segment . bss'
				]
		crap = 'ADD EDX, {}'.format('0')
		second = ['section .text',
				  'global _start',
				  'print :', 
				  'POP EBX',
				  'POP EAX',
				  'PUSH EBX',
				  'XOR ESI , ESI',
				  'print_dec :',
				  'MOV EDX, 0',
				  'MOV EBX, 0x000A',
				  'DIV EBX',
				   crap,
				  'PUSH EDX',
				  'INC ESI',
				  'CMP EAX, 0',
				  'JZ print_next',
				  'JMP print_dec',
				  'print_next :',
				  'CMP ESI , 0',
				  'JZ print _ exit',
				  'DEC ESI',
				  'MOV EAX, SYS_WRITE',
				  'MOV EBX, STDOUT',
				  'POP ECX',
				  'MOV [res] , ECX',
				  'MOV ECX, res',
				  'MOV EDX, 1',
				  'INT 0 x80',
				  'JMP prin t_next',
				  'print _ exit :',
				  'RET',
				  'binop_je :',
				  'JE binop_true',
				  'JMP binop_ false',
				  'binop_jg :',
				  'JG binop_true',
				  'JMP binop_false',
				  'binop_jl :',
				  'JL binop_true',
				  'JMP binop_false',
				  'binop_false :',
				  'MOV EBX, False',
				  'JMP binop_exit',
				  'binop_true :',
				  'MOV EBX, True',
				  'bin op_exit :',
				  'RET',
				  '_ start :'
				]

		for v in range(0,len(self.var)):
			self.var[v] = self.var[v] + " RESD 1"

		assCode = first +  self.var + second + self.code
		f = open("testfile.asm","w")
		for line in assCode:
			f.write(line + "\n")
		f.close()

def main():
	symbolTable = SymbolTable()
	symbolTable.id = Id.getNew("st")

	with open("testes.c") as f:
		content = f.readlines()
	content = [x.strip() for x in content] 

	code = ""
	for line in content:
		code+=line

	root = Analyser(code).statments()
	root.Evaluate(symbolTable)

	t = AssemblyCode(var, Asscode)
	t.Buildfile()

if __name__ == "__main__":
	main()