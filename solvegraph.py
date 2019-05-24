from maze2graph import maze2graph

startNode = None
endNode = None
edges = None
edgeMap = {}
costMap = {}

def costToEnd(i):
	if i == endNode:
		return 0
	
	if i in costMap:
		return costMap[i][0]

	costMap[i] = None

	minCost = 9999999
	bestTarget = None
	for j in edgeMap[i]:
		if j in costMap and costMap[j] == None:
			continue # avoid cycles

		cost = costToEnd(j)
		if cost < minCost:
			minCost = cost
			bestTarget = j

	if bestTarget == None:
		return minCost

	cost, direction = edgeMap[i][bestTarget]
	costMap[i] = (cost + minCost, bestTarget, direction)

	return costMap[i][0]

def load_graph(path):
	global startNode, endNode, edges

	startNode, endNode, edges = maze2graph(path)

	for edge in edges:
		i, j, distance, direction = edge
		if i not in edgeMap:
			edgeMap[i] = {}

		edgeMap[i][j] = (distance, direction) 

def calculate_path():
	global costMap

	costMap = {}
	costToEnd(startNode)

	path = []
	curr = startNode
	while curr != endNode:
		cost, target, direction = costMap[curr]
		path.append((curr, direction))
		curr = target

	return path

def delete_edge(i, j):
	del edgeMap[i][j]
	del edgeMap[j][i]

	calculate_path()

if __name__ == '__main__':
	load_graph("maze.png")
	path = calculate_path()
	print(path)

	delete_edge(31, 32)
	path = calculate_path()
	print(path)