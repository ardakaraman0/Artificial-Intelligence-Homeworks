# Arda Karaman 2237568

import copy

class State:
    def __init__(self, env, obstacles, goals, reward, actions, gamma, epsilon, iteration):
        self.iteration = iteration
        self.epsilon = epsilon
        self.gamma = gamma
        self.actions = actions
        self.reward = reward
        self.goals = goals
        self.obstacles = obstacles
        self.env = env


class Cell:
    def __init__(self, pos, value, rotation, up, down, left, right, isObstacle, isExit):
        self.isExit = isExit
        self.isObstacle = isObstacle
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.pos = pos
        self.value = value
        self.rotation = rotation


class Goal:
    def __init__(self, pos, reward):
        self.reward = reward
        self.pos = pos


def SolveMDP(method_name, problem_file_name):
    with open(problem_file_name, mode='r') as f:
        env, obsState, goal, reward, action, gamma, epsilon, iteration = False, False, False, False, False, False, False, False
        envV, obsStateV, goalV, rewardV, actionV, gammaV, epsilonV, iterationV = None, [], [], None, [], None, None, None
        for line in f:
            line = line.removesuffix('\n')
            if line == '[environment]':
                env = True
                continue
            if line == '[obstacle states]':
                obsState = True
                continue
            if line == '[goal states]':
                goal = True
                continue
            if line == '[reward]':
                reward = True
                continue
            if line == '[action noise]':
                action = True
                continue
            if line == '[gamma]':
                gamma = True
                continue
            if line == '[epsilon]':
                epsilon = True
                continue
            if line == '[iteration]':
                iteration = True
                continue
            if env:
                envV = tuple(line.split(' '))
                envV = [int(i) for i in envV]
                env = False
                continue
            if obsState:
                line = line.split('|')
                for c in line:
                    obsStateV.append((int(c[1]), int(c[3])))
                obsState = False
                continue
            if goal:
                line = line.split('|')
                for c in line:
                    c = c.split(':')
                    goalV.append(Goal((int(c[0][1]), int(c[0][3])), float(c[1])))
                goal = False
                continue
            if reward:
                rewardV = float(line)
                reward = False
                continue
            if gamma:
                gammaV = float(line)
                action = False
                gamma = False
                continue
            if action:
                actionV.append(float(line))
                continue
            if epsilon:
                epsilonV = float(line)
                epsilon = False
                continue
            if iteration:
                iterationV = int(line)
                iteration = False
                continue

        state = State(envV, obsStateV, goalV, rewardV, actionV, gammaV, epsilonV, iterationV)
        board = InitBoard(state)
        if method_name == "ValueIteration":
            ValueIt(state, board)
            U = {}
            policy = {}
            for i in board:
                for j in i:
                    if not j.isObstacle:
                        U[j.pos] = "{:.2f}".format(j.value)
                        policy[j.pos] = j.rotation
            return U, policy
        if method_name == "PolicyIteration":
            PolicyIt(state, board)
            U = {}
            policy = {}
            for i in board:
                for j in i:
                    if not j.isObstacle:
                        U[j.pos] = "{:.2f}".format(j.value)
                        policy[j.pos] = j.rotation
            return U, policy
    return


def FindReward(state: State, pos):
    for goal in state.goals:
        if goal.pos == pos:
            return goal.reward
    return 0.0


def InitBoard(state: State):
    board = []
    for i in range(state.env[0]):
        board.append([])
        for j in range(state.env[1]):
            if (i, j) in state.obstacles:
                cell = Cell((i, j), 0.0, "", None, None, None, None, True, False)
            else:
                val = FindReward(state, (i, j))
                cell = Cell((i, j), val, "", None, None, None, None, False, True if val is not 0.0 else False)
            board[i].append(cell)

    for i in range(state.env[0]):
        for j in range(state.env[1]):
            if (i, j) not in state.obstacles:
                board[i][j].up = board[i - 1][j] if i >= 1 else None
                board[i][j].down = board[i + 1][j] if i <= len(board) - 2 else None
                board[i][j].left = board[i][j - 1] if j >= 1 else None
                board[i][j].right = board[i][j + 1] if j <= len(board[i]) - 2 else None
    return board


def CheckValue(state: State, current: Cell, nextCell: Cell, up=False, down=False, left=False, right=False):
    if nextCell is None:
        return 0.0, ""
    rot = ""
    T = (nextCell.value * state.gamma + state.reward) * state.actions[0]
    T_1 = None
    T_2 = None
    if up:
        rot = "^"
        if current.left:
            T_1 = (current.left.value * state.gamma + state.reward) * state.actions[1]
        if current.right:
            T_2 = (current.right.value * state.gamma + state.reward) * state.actions[2]
    if down:
        rot = "V"
        if current.right:
            T_1 = (current.right.value * state.gamma + state.reward) * state.actions[1]
        if current.left:
            T_2 = (current.left.value * state.gamma + state.reward) * state.actions[2]
    if left:
        rot = "<"
        if current.down:
            T_1 = (current.down.value * state.gamma + state.reward) * state.actions[1]
        if current.up:
            T_2 = (current.up.value * state.gamma + state.reward) * state.actions[2]
    if right:
        rot = ">"
        if current.up:
            T_1 = (current.up.value * state.gamma + state.reward) * state.actions[1]
        if current.down:
            T_2 = (current.down.value * state.gamma + state.reward) * state.actions[2]

    if T_1 is None:
        T_1 = (current.value * state.gamma + state.reward) * state.actions[1]
    if T_2 is None:
        T_2 = (current.value * state.gamma + state.reward) * state.actions[2]
    T += T_1 + T_2
    print(T)
    return T, rot


def k(v):
    return v[0]


def CheckEpsilon(state: State, oldBoard, newBoard):
    for i in range(len(oldBoard)):
        for j in range(len(oldBoard[i])):
            if not oldBoard[i][j].isExit and not oldBoard[i][j].isObstacle:
                if abs(oldBoard[i][j].value - newBoard[i][j].value) > state.epsilon:
                    return False
    return True


def ValueIt(state: State, board):
    while True:
        oldBoard = copy.deepcopy(board)
        for i in board:
            for j in i:
                currentCell: Cell = j
                if currentCell.isExit:
                    continue
                newV = max(CheckValue(state, currentCell, currentCell.up, up=True),
                           CheckValue(state, currentCell, currentCell.down, down=True),
                           CheckValue(state, currentCell, currentCell.left, left=True),
                           CheckValue(state, currentCell, currentCell.right, right=True), key=k)
                currentCell.value = newV[0]
                currentCell.rotation = newV[1]
        if CheckEpsilon(state, oldBoard, board):
            return


def PolicyIt(state: State, board):
    for x in range(state.iteration):
        for i in board:
            for j in i:
                currentCell: Cell = j
                if currentCell.isExit:
                    continue
                newV = max(CheckValue(state, currentCell, currentCell.up, up=True),
                           CheckValue(state, currentCell, currentCell.down, down=True),
                           CheckValue(state, currentCell, currentCell.left, left=True),
                           CheckValue(state, currentCell, currentCell.right, right=True), key=k)
                currentCell.value = newV[0]
                currentCell.rotation = newV[1]
    return


# print(SolveMDP("PolicyIteration", "HW 4 Problem and Output Files-20211231/mdp2.txt"))
