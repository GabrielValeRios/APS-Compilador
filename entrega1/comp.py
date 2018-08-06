with open('testes.txt') as f:
    content = f.readlines()
content = [x.strip().replace(" ","") for x in content]

class solver():
	def __init__(self,content):
		op = content + 'k'
		flagnum = True
		somar = False
		subtrair = False
		num = ['','']
		resposta = []
		for simb in op:
			if (simb.isdigit()) and (flagnum == True):
				num[0] += simb
			if simb == '+':
				somar = True
				flagnum = False
			if simb == '-':
				subtrair = True
				flagnum = False
			if (simb.isdigit()) and (flagnum == False):
				num[1] += simb
			if ((simb == '+') or (simb == '-') or (simb == 'k')) and num[1] != '':
				if somar == True:
					num[0] = (int(num[0]) + int(num[1]))
					somar = False
				elif subtrair == True:
					num[0] = (int(num[0]) - int(num[1]))
					subtrair = False
				num[1] = ''
		print(num[0])
		flagnum = True

for i in content:
	solver(i)