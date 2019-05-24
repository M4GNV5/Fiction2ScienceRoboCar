from maze2graph import maze2graph

class GraphSolver:
	def __init__(self):
		self.startNode = None
		self.endNode = None
		self.edges = None
		self.edgeMap = {}
		self.costMap = {}

	def costToEnd(self, i):
		if i == self.endNode:
			return 0
		if i in self.costMap:
			return self.costMap[i][0]

		self.costMap[i] = None

		minCost = 9999999
		bestTarget = None
		for j in self.edgeMap[i]:
			if j in self.costMap and self.costMap[j] == None:
				continue # avoid cycles

			cost = self.costToEnd(j)
			if cost < minCost:
				minCost = cost
				bestTarget = j

		if bestTarget == None:
			del self.costMap[i]
			return minCost

		cost, direction = self.edgeMap[i][bestTarget]
		self.costMap[i] = (cost + minCost, bestTarget, direction)

		return self.costMap[i][0]

	def load_graph(self, path):
		self.startNode, self.endNode, self.edges = maze2graph(path)

		for edge in self.edges:
			i, j, distance, direction = edge
			if i not in self.edgeMap:
				self.edgeMap[i] = {}

			self.edgeMap[i][j] = (distance, direction) 

	def calculate_path(self):

		self.costMap = {}
		self.costToEnd(self.startNode)

		path = []
		curr = self.startNode
		while curr != self.endNode:
			cost, target, direction = self.costMap[curr]
			path.append((curr, direction))
			curr = target

		return path

	def delete_edge(self, i, j):
		del self.edgeMap[i][j]
		del self.edgeMap[j][i]

		calculate_path()

if __name__ == '__main__':
	solver = GraphSolver()
	solver.load_graph("maze.png")
	path = solver.calculate_path()
	print(path)

	solver = GraphSolver()
	solver.load_graph("dataset/mazes/3.png")
	path = solver.calculate_path()
	print(path)
