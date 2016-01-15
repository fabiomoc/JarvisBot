from pygoogle import pygoogle

def search(nome):
	dis = pygoogle(nome)
	dis.pages = 1
	print('dis is',dis.cont())
	result = dis.cont()
	return result