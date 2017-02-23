
import heapq

map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,1,1,1,1,1,1,0,1],
    [1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Problem:
    def __init__(self):
        self.goal = (11, 4)

    def getStartState(self):
        return (1,1)

    def isGoalState(self, state):
        return state[0] == self.goal[0] and state[1] == self.goal[1]

    def getActions(self, state):
        x = state[0]
        y = state[1]

        actions = []
        if map[y][x-1] != 1:
            actions.append('left')
        if map[y][x+1] != 1:
            actions.append('right')
        if map[y-1][x] != 1:
            actions.append('up')
        if map[y+1][x] != 1:
            actions.append('down')

        return actions

    def doAction(self, state, action):
        if action == 'left':
            return (state[0]-1, state[1])

        if action == 'right':
            return (state[0]+1, state[1])

        if action == 'up':
            return (state[0], state[1]-1)

        if action == 'down':
            return (state[0], state[1]+1)

    def getCost(self, state, action):
        return 1

    def heuristic(self, state):
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

class Fringe:
    def isEmpty(self):
        return True

    def push(self, state):
        pass

    def pop(self):
        pass

class Stack:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def push(self, state):
        self.list.insert(0, state)

    def pop(self):
        return self.list.pop(0)

class Queue:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def push(self, state):
        self.list.append(state)

    def pop(self):
        return self.list.pop(0)

class Ucs:
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return len(self.list) == 0

    def push(self, state):
        heapq.heappush(self.list, (state[1], state))

    def pop(self):
        return heapq.heappop(self.list)[1]

class Astar:
    def __init__(self, heuristic):
        self.list = []
        self.heuristic = heuristic

    def isEmpty(self):
        return len(self.list) == 0

    def push(self, state):
        heapq.heappush(self.list, (state[1] + self.heuristic(state[0]), state))

    def pop(self):
        return heapq.heappop(self.list)[1]

class GraphSearch:

    def __init__(self, fringe, problem):
        self.fringe = fringe
        self.problem = problem

    def find(self):
        startState = self.problem.getStartState()
        if self.problem.isGoalState(startState):
            return []

        expansions = 0
        costs = {}
        paths = {}

        costs[startState] = 0
        self.fringe.push((startState, 0))

        while not self.fringe.isEmpty():
            (state, totalCost) = self.fringe.pop()

            # costs dictionary contains a newer version that is faster. just skip this one.
            if costs[state] < totalCost:
                continue

            if self.problem.isGoalState(state):
                print('Found goal after', expansions, 'expansions')
                path = []
                (prevState, prevAction) = paths[state]
                path.append((prevState, prevAction))
                while prevState in paths:
                    (prevState, prevAction) = paths[prevState]
                    path.append((prevState, prevAction))
                path.reverse()
                return path


            actions = self.problem.getActions(state)
            for action in actions:
                nextState = self.problem.doAction(state, action)
                actionCost = self.problem.getCost(state, action)

                nextCost = totalCost + actionCost
                isNewState = nextState not in costs
                if isNewState or nextCost < costs[nextState]:
                    costs[nextState] = nextCost
                    paths[nextState] = (state, action)

                if isNewState:
                    expansions += 1
                    self.fringe.push((nextState, nextCost))

        return []

problem = Problem()
fringe = Astar(problem.heuristic)
#fringe = Stack()
graphSearch = GraphSearch(fringe, problem)
for (state, action) in graphSearch.find():
    print(state, action)
