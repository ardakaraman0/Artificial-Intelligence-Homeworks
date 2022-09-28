def InformedSearch(method_name, problem_file_name):
    with open(problem_file_name, mode='r') as f:
        isPuzzle = True
        if problem_file_name.startswith("maze"):
            isPuzzle = False
        start, end, board, target, nodeBoard, nodeTarget = initBoard(isPuzzle, f)

        solution = []
        processedNodes = []
        if method_name == "AStar":
            if not isPuzzle:
                SetHeuristic(nodeBoard, end)
                queue = [start]
                x=0
                while queue:
                    cursor = queue.pop()
                    cursor.visited = True
                    processedNodes.append((cursor.x,cursor.y))
                    if cursor.x == end.x and cursor.y == end.y:
                        break
                    GetAdjacent(cursor, nodeBoard, queue)
                    UpdateFandSort(queue)
                    SameFValResort(queue)
                    x+=1

                temp = end
                while temp is not None:
                    solution.append((temp.x, temp.y))
                    temp = temp.comesBefore

                solution.reverse()
                if len(solution) == 1:
                    return None
            else:
                SetHeuristicPuzzle(nodeBoard, nodeTarget)
                # Managed to set the heuristics

            return solution, processedNodes, end.g, end.g
        if method_name == "UCS":
            if not isPuzzle:
                queue = [start]
                processedNodes = []
                x=0
                while queue:
                    cursor = queue.pop()
                    cursor.visited = True
                    processedNodes.append((cursor.x,cursor.y))
                    GetAdjacent(cursor, nodeBoard, queue)
                    if queue:
                        UpdateFandSort(queue)
                        SameFValResortUCS(queue)
                    x+=1
                temp = end
                while temp is not None:
                    solution.append((temp.x, temp.y))
                    temp = temp.comesBefore

                solution.reverse()
            else:
                return None

            return solution, processedNodes, end.g, end.g
        return


class Node:
    def __init__(self, x, y, g, h, isStart, isEnd, val, visited, comesBefore):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.isEnd = isEnd
        self.isStart = isStart
        self.val = val
        self.visited = visited
        self.comesBefore = comesBefore


class TargetNode:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val


def initBoard(isPuzzle, file):
    nodeBoard = []
    board = []

    if not isPuzzle:  # Maze
        i = 0
        for line in file:
            if i == 0:
                _start = int(line[line.find("(") + 1:line.find(",")]), int(line[line.find(",") + 1:line.find(")")])
                i += 1
                continue
            if i == 1:
                _end = int(line[line.find("(") + 1:line.find(",")]), int(line[line.find(",") + 1:line.find(")")])
                i += 1
                continue
            row = []
            row[:0] = line.removesuffix("\n")
            board.append(row)

        for y in range(len(board)):
            temprow = []
            for x in range(len(board[0])):
                temp = True if board[y][x] != "#" else False
                newNode = Node(x, y, 0, 0, False, False, temp, False, None)
                if x == _start[0] and y == _start[1]:
                    newNode.isStart = True
                    startNode = newNode
                if x == _end[0] and y == _end[1]:
                    newNode.isEnd = True
                    endNode = newNode
                temprow.append(newNode)
            nodeBoard.append(temprow)

        return startNode, endNode, board, None, nodeBoard, None

    else:  # EightPuzzle
        target = []
        isboard = True
        for line in file:
            row = line.removesuffix("\n").split(" ")
            if row == ['']:
                isboard = False
                continue
            if isboard:
                board.append(row)
            else:
                target.append(row)

        nodeTarget = [None] * len(target) * len(target[0])

        for y in range(len(target)):
            for x in range(len(target[0])):
                nodeTarget[int(target[y][x])] = TargetNode(x, y, int(target[y][x]))

        for y in range(len(board)):
            temprow = []
            for x in range(len(board[0])):
                tmp = True if int(board[y][x]) == 0 else False
                temprow.append(
                    Node(x, y, 0, abs(x - nodeTarget[int(board[y][x])].x) + abs(y - nodeTarget[int(board[y][x])].y),
                         tmp, False, int(board[y][x]), False, None))
            nodeBoard.append(temprow)

        return None, None, board, target, nodeBoard, nodeTarget


def FindLowestFCost(queue: [Node]):
    fcost = queue[0].f
    returnVal = queue[0]
    for node in queue:
        if node.f < fcost:
            returnVal = node
            fcost = node.f
    return returnVal


def SetHeuristic(board: [Node], endNode):
    for row in board:
        for node in row:
            if node.val:
                node.h = abs(node.x - endNode.x) + abs(node.y - endNode.y)
    return None

def SetHeuristicPuzzle(board: [Node], nodeTarget):
    for row in board:
        for node in row:
            node.h = abs(node.x - nodeTarget[node.val].x) + abs(node.y - nodeTarget[node.val].y)


def GetAdjacent(current: Node, board: [Node], queue):
    up, down, right, left = None, None, None, None
    try:
        up = board[current.y + 1][current.x]
    except IndexError:
        up = None
    try:
        if current.y > 1:
            down = board[current.y - 1][current.x]
    except IndexError:
        down = None
    try:
        if current.x > 1:
            left = board[current.y][current.x - 1]
    except IndexError:
        left = None
    try:
        right = board[current.y][current.x + 1]
    except IndexError:
        right = None

    if up is not None and up.val and not up.visited:
        if UpdateGCost(current, up):
            queue.append(up)
            up.comesBefore = current

    if down is not None and down.val and not down.visited:
        if UpdateGCost(current, down):
            queue.append(down)
            down.comesBefore = current

    if right is not None and right.val and not right.visited:
        if UpdateGCost(current, right):
            queue.append(right)
            right.comesBefore = current

    if left is not None and left.val and not left.visited:
        if UpdateGCost(current, left):
            queue.append(left)
            left.comesBefore = current


def UpdateGCost(current, node):
    if node.g == 0:
        node.g = current.g + 1
        return True
    if node.g > current.g + 1:
        node.g = current.g + 1
        return False


def getF(node):
    return node.f


def getH(node):
    return node.h


def getG(node):
    return node.g


def UpdateFandSort(queue):
    for node in queue:
        node.f = node.g + node.h
    queue.sort(key=getF)


def SameFValResort(queue):
    val = queue[0].f
    l = []
    for i in range(len(queue)):
        if queue[i].f == val:
            l.append(queue[i])
        else:
            break

    l.sort(key=getH)
    queue[0:len(l)] = l

def SameFValResortUCS(queue):
    val = queue[0].f
    l = []
    for i in range(len(queue)):
        if queue[i].f == val:
            l.append(queue[i])
        else:
            break

    l.sort(key=getG)
    queue[0:len(l)] = l


print(InformedSearch("AStar", "eightpuzzle1.txt"))
