import random
import copy


# Student name & surname: Arda Karaman
# Student ID: 2237568


class State:
    def __init__(self, env, obstacles, goals, reward, actions, gamma, epsilon, iteration, start):
        self.start = start
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


def SolveMDP(method_name, problem_file, seed=123):
    random.seed(seed)

    # Augment the data
    with open(problem_file, mode='r') as f:
        env, obsState, goal, reward, action, gamma, epsilon, iteration, startState = False, False, False, False, False, False, False, False, False
        envV, obsStateV, goalV, rewardV, actionV, gammaV, epsilonV, iterationV, startStateV = None, [], [], None, [], None, None, None, None
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
            if line == '[start state]':
                startState = True
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
            if startState:
                startStateV = (int(line[1]), int(line[3]))
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
    U = None
    policy = None
    if method_name == "TD(0)":
        x = 0
        return U, policy
    elif method_name == "Q-learning":
        x = 0
        return U, policy
    else:
        return "Unidentified method name."


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
