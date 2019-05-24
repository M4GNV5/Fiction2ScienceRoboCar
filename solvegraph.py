from maze2graph import maze2graph

class GraphSolver:
	def __init__(self):
		self.startNode = None
		self.endNode = None
		self.edges = None
		self.edgeMap = {}
		self.costMap = {}

	def calculate_cost(self, i, cost, target):
		if i in self.costMap and self.costMap[i][0] < cost:
			return

		self.costMap[i] = (cost, target)

		for j in self.edgeMap[i]:
			distance, direction = self.edgeMap[i][j]
			self.calculate_cost(j, cost + distance, i)

	def load_graph(self, path):
		self.startNode, self.endNode, self.edges = maze2graph(path)

		for i, j, distance, direction in self.edges:
			if i not in self.edgeMap:
				self.edgeMap[i] = {}

			self.edgeMap[i][j] = (distance, direction) 

	def calculate_path(self):
		self.costMap = {}
		self.calculate_cost(self.endNode, 0, None)

		path = []
		curr = self.startNode
		while curr != self.endNode:

			minCost = 9999
			bestTarget = None
			for j in self.edgeMap[curr]:
				cost, target = self.costMap[j]

				if cost < minCost:
					minCost = cost
					bestTarget = j

			distance, direction = self.edgeMap[curr][bestTarget]
			path.append((curr, direction))
			curr = bestTarget

		return path

	def delete_edge_and_set_start(self, i, j):
		del self.edgeMap[i][j]
		del self.edgeMap[j][i]

		self.startNode = i

if __name__ == '__main__':
	solver = GraphSolver()
	solver.load_graph("maze.png")
	path = solver.calculate_path()
	print(path)

	solver = GraphSolver()
	solver.load_graph("dataset/mazes/3.png")
	path = solver.calculate_path()
	print(path)
