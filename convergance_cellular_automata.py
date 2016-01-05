
class CA:
	def __init__(self, name='CA - 2D', rows=10, columns=10):
		self.nextGeneration = None
		self.states = {}
		self.name = name
		self.rows = rows
		self.columns = columns
		self.map = [[0 for j in range(columns)] for i in range(rows)]

	def setColor(self, dic):
		self.states = dic

	def setNextGeneration(self, NGFunction=None):
		self.nextGeneration = NGFunction

	def getMap(self):
		return self.map

	def tick(self):
		if self.nextGeneration is None:
			return 0

		for i in range(self.rows):
			for j in range(self.columns):
				self.map[i][j] = self.nextGeneration(i, j, self.map)

		return 1

	def draw(self):
		# uses self.tick and self.states
		pass




def nextGen(i, j, map):
	return 1 if not map[i][j] else 0

myCa = CA('conway game of lime', 100, 100)
myCa.setColor({0: 'black', 1: 'white'})
myCa.setNextGeneration(nextGen)

