import cv2

img = cv2.imread("maze.png")

height, width, c = img.shape
width = int(width / 2)
height = int(height / 2)
img = cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)

colored = img

img = cv2.inRange(img, (0, 0, 0), (20, 20, 20))
img = cv2.bitwise_not(img)

nodeCount = 0
nodes = {}
edges = []
unvisited = []

def isBlack(x, y):
	if x < 0 or x >= width \
		or y < 0 or y >= height:
		return False

	return img[y, x] == 0

def isNode(x, y):
	if isBlack(x, y):
		east = isBlack(x + 1, y)
		west = isBlack(x - 1, y)
		north = isBlack(x, y + 1)
		south = isBlack(x, y - 1)

		blackSum = sum([
			1 if east else 0,
			1 if west else 0,
			1 if north else 0,
			1 if south else 0,
		])

		return (blackSum == 1 or blackSum > 2) \
			or ((east or west) and (north or south)) 

def addNode(x, y):
	global nodeCount
	index = nodeCount
	nodeCount += 1

	nodes[(x, y)] = index
	unvisited.append((x, y))
	return index

def checkDirection(x, y, dx, dy):
	global nodeCount

	x += dx
	y += dy
	distance = 1

	if not isBlack(x, y):
		return None

	while not isNode(x, y):
		x += dx
		y += dy
		distance += 1

	if (x, y) in nodes:
		other = nodes[(x, y)]
	else:
		other = addNode(x, y)
	return (other, distance, x, y)

def checkAndCreateEdge(x, y, dx, dy):
	ret = checkDirection(x, y, dx, dy)

	if ret is None:
		return

	end, distance, endX, endY = ret
	start = nodes[(x, y)]

	if (endX, endY) in unvisited:
		edges.append((start, end, distance))

def findStart():
	for y in range(0, height):
		for x in range(0, width):
			if isNode(x, y):
				return addNode(x, y)

def findEnd():
	for y in range(0, height):
		y = height - y - 1
		for x in range(0, width):
			if isNode(x, y):
				return addNode(x, y)

startNode = findStart()
endNode = findEnd()

while len(unvisited) > 0:
	x, y = unvisited.pop()

	checkAndCreateEdge(x, y, 1, 0)
	checkAndCreateEdge(x, y, -1, 0)
	checkAndCreateEdge(x, y, 0, 1)
	checkAndCreateEdge(x, y, 0, -1)
	
print("count - %d" % len(edges))
print("start - %d" % startNode)
print("end - %d" % endNode)
for i, j, d in edges:
	print("%d-%d,%d,%d" % (i, j, d, 2))

'''
for i, j, d in edges:
	for key in nodes:
		if nodes[key] == i:
			xi, yi = key
		if nodes[key] == j:
			xj, yj = key

	img = colored.copy()
	cv2.line(img, (xi, yi), (xj, yj), (255, 0, 0), 2)
	img = cv2.resize(img, (width * 8, height * 8), interpolation=cv2.INTER_NEAREST)
	cv2.putText(img, ("%d-%d,%d,2" % (i, j, d)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)

	cv2.imshow("output", img)
	key = cv2.waitKey(0)
	if key == ord('q'):
		break
'''