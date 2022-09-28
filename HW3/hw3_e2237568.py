# Arda Karaman e2237568
# There is a bug in the alpha-beta method implementation for the ticktacktoe game.

p_infinity = float('inf')
n_infinity = float('-inf')


class Board:
    def __init__(self, boardState: list, actions: list, depth: int, point: float, turn: str, isMax: bool,
                 alphaBetaVal: float, route, chosenAction):
        self.chosenAction = chosenAction
        self.route = route
        self.alphaBetaVal = alphaBetaVal
        self.isMax = isMax
        self.turn = turn
        self.point = point
        self.depth = depth
        self.actions = actions
        self.boardState = boardState

    def PrintBoardState(self):
        res = ''
        for j in self.boardState:
            for i in j:
                res += i
        return res


class ActionNode:
    def __init__(self, name, placeholder, value):
        self.placeholder = placeholder
        self.name = name
        self.value = value


class TreeNode:
    def __init__(self, name, actions: [ActionNode], depth: int, point, isMax: bool, alphaBetaVal: float):
        self.name = name
        self.actions = actions
        self.depth = depth
        self.point = point
        self.alphaBetaVal = alphaBetaVal
        self.isMax = isMax


def Find(node: ActionNode, nodes: list):
    for x in nodes:
        if x.name == node.name:
            return x


def AlphaBetaTree(nodes: list, tree: TreeNode, q: list, pruneFactor: float):
    val, chosenactionname = 0, ''
    for n in tree.actions:
        q.append(n.name)
        if n.value == 0:
            nextTree: TreeNode = Find(n, nodes)
            points, action, _ = AlphaBetaTree(nodes, nextTree, q, tree.alphaBetaVal)
            if tree.isMax:
                if points > tree.alphaBetaVal:
                    tree.alphaBetaVal = points
                if val < points:
                    val = points
                    chosenactionname = n.placeholder
            else:
                if points < tree.alphaBetaVal:
                    tree.alphaBetaVal = points
                if val > points:
                    val = points
                    chosenactionname = n.placeholder
        else:
            if tree.isMax:
                if val > pruneFactor:
                    break
                if val == 0:
                    val = n.value
                    chosenactionname = n.placeholder
                if val < n.value:
                    val = n.value
                    chosenactionname = n.placeholder
            else:
                if val < pruneFactor:
                    break
                if val == 0:
                    val = n.value
                    chosenactionname = n.placeholder
                if val > n.value:
                    val = n.value
                    chosenactionname = n.placeholder
    tree.alphaBetaVal = val
    return val, chosenactionname, q


def MinimaxTree(nodes: list, tree: TreeNode, q: list):
    val, chosenactionname = 0, ''
    for n in tree.actions:
        q.append(n.name)
        if n.value == 0:
            points, action, _ = MinimaxTree(nodes, Find(n, nodes), q)
            if tree.isMax:
                if val < points:
                    val = points
                    chosenactionname = n.placeholder
            else:
                if val > points:
                    val = points
                    chosenactionname = n.placeholder
        else:
            if tree.isMax:
                if val < n.value:
                    val = n.value
                    chosenactionname = n.placeholder
            else:
                if val == 0:
                    val = n.value
                    chosenactionname = n.placeholder
                if val > n.value:
                    val = n.value
                    chosenactionname = n.placeholder

    return val, chosenactionname, q

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Bug in the Alpha-Beta algorithm for the ticktacktoe game
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def AlphaBetaBoard(board: Board, que: list, pruneFactor: float, isMax: bool):
    if isMax:
        if board.point < pruneFactor:
            return None, None
    else:
        if board.point > pruneFactor:
            return None, None

    if len(board.actions) == 0:
        que.append(board.PrintBoardState())
        return board.point, board
    chosenVal = 0
    chosenAction = None
    que.append(board.PrintBoardState())
    for node in board.actions:
        if AlphaBetaBoard(node, que, board.alphaBetaVal, board.isMax) != (None, None):
            node.point, solution = AlphaBetaBoard(node, que, board.alphaBetaVal, board.isMax)
        else:
            continue
        if board.isMax:
            if chosenVal <= node.point:
                board.chosenAction = node
                chosenVal = node.point
                board.alphaBetaVal = chosenVal
        else:
            if chosenVal >= node.point:
                board.chosenAction = node
                chosenVal = node.point
                board.alphaBetaVal = chosenVal
    return chosenVal, board.chosenAction


def MinimaxBoard(board: Board, que: list):
    if len(board.actions) == 0:
        que.append(board.PrintBoardState())
        return board.point, board
    chosenVal = -10 if board.isMax else 10
    chosenAction = None
    que.append(board.PrintBoardState())
    for node in board.actions:
        node.point, solution = MinimaxBoard(node, que)
        if board.isMax:
            if chosenVal <= node.point:
                board.chosenAction = node
                chosenVal = node.point
        else:
            if chosenVal >= node.point:
                board.chosenAction = node
                chosenVal = node.point

    return chosenVal, board.chosenAction


def findInActionsParent(nodes: [TreeNode], _name):
    for t in nodes:
        for n in t.actions:
            if n.name == _name:
                return t


def findInActionsAction(nodes: [TreeNode], _name):
    for t in nodes:
        for n in t.actions:
            if n.name == _name:
                return n


def CreateTree(board: Board, cellCount):
    if cellCount == 0:
        return
    nextBoards = []
    for x in range(cellCount):
        nextBoards.append([row[:] for row in board.boardState])

    locations = []
    count = 0
    for j in range(3):
        for i in range(3):
            if board.boardState[j][i] == ' ':
                nextBoards[count][j][i] = 'X' if board.turn == 'X' else 'O'
                locations.append((j, i))
                count += 1

    i = 0
    for b in nextBoards:
        newBoard = Board(b, [], board.depth + 1, CheckWhoWon(b, board.depth + 1), 'O' if board.turn == 'X' else 'X',
                         not board.isMax,
                         p_infinity if not board.isMax == max else n_infinity, locations[i], None)
        board.actions.append(newBoard)
        if newBoard.point == 0:
            CreateTree(newBoard, cellCount - 1)
        i += 1
    return


winConditions = [((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                 ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                 ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]


def CheckWhoWon(board: list, depth):
    for cond in winConditions:
        if board[cond[0][0]][cond[0][1]] == board[cond[1][0]][cond[1][1]] and \
                board[cond[2][0]][cond[2][1]] == board[cond[1][0]][cond[1][1]]:
            if board[cond[0][0]][cond[0][1]] == 'X':
                return 5 - (0.01 * (depth - 1))
            elif board[cond[0][0]][cond[0][1]] == 'O':
                return -5
    return 0


def SolveGame(method_name, problem_file_name, player_type):
    with open(problem_file_name, mode='r') as f:
        if problem_file_name.startswith("sets/tictactoe"):
            matrix = []
            emptyCellCount = 0
            j = 0
            for line in f:
                matrix.append([])
                line = line.removesuffix('\n')
                for char in line:
                    if char == ' ':
                        emptyCellCount += 1
                    matrix[j].append(char)
                j += 1

            newBoard = Board(matrix, [], 0, 0, 'X', player_type == "MAX",
                             p_infinity if player_type == max else n_infinity, None, None)

            CreateTree(newBoard, emptyCellCount)

            solv = None
            q = []
            solq = []
            if method_name == "Minimax":
                solv, node = MinimaxBoard(newBoard, q)
            else:
                solv, node = AlphaBetaBoard(newBoard, q, newBoard.alphaBetaVal, newBoard.isMax)
            if not solv and not node:
                return None
            return solv, (node.route[1], node.route[0]), q

        else:
            nodes: [TreeNode] = []
            name = f.readline().removesuffix("\n")
            nodes.append(
                TreeNode(name, [], 0, 0, player_type == "MAX", p_infinity if player_type == max else n_infinity))

            for line in f:
                elements = line.removesuffix("\n").split(' ')
                if len(elements) == 3:
                    if elements[0] == nodes[-1].name:
                        nodes[-1].actions.append(ActionNode(elements[1], elements[2], 0))
                    else:
                        parent = findInActionsParent(nodes, elements[0])
                        nodes.append(
                            TreeNode(elements[0], [ActionNode(elements[1], elements[2], 0)], parent.depth + 1, 0,
                                     not parent.isMax, 0))
                else:
                    elements = line.removesuffix("\n").split(":")
                    node = findInActionsAction(nodes, elements[0])
                    node.value = int(elements[1])

            solv = None
            q = []
            if method_name == "Minimax":
                solv, action, q = MinimaxTree(nodes, nodes[0], q)
            else:
                solv, action, q = AlphaBetaTree(nodes, nodes[0], q, nodes[0].alphaBetaVal)

            return solv, action, q

print(SolveGame("Minimax", "sets/tictactoe3.txt", "MAX"))
