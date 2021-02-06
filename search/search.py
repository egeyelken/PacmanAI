# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    #Frontier is a LIFO Stack.
    frontier = util.Stack()

    state = problem.getStartState()
    expandedNodes = set()

    # Initialize the frontier using the initial state.
    frontier.push((state, []))

    while True:
        # 1)If the frontier is empty, return failure.
        if frontier.isEmpty():
            return "Failure"
        # 2)Choose a leaf node and remove it from the frontier.
        node, path = frontier.pop()
        # 3)If the node returns a goal state, return the corresponding solution.
        if problem.isGoalState(node):
            return path
        # 4)Expand the chosen node, adding the resulting nodes to the frontier.
        expandedNodes.add(node)
        successors = problem.getSuccessors(node)
        for node, action, _ in successors:
            if node not in expandedNodes:
                frontier.push((node, path + [action]))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    # Frontier is a FIFO Queue.
    frontier = util.Queue()

    state = (problem.getStartState(), {})
    node = None
    expandedNodes = set()
    path = list()

    # Initialize the frontier using the initial state.
    frontier.push(state)

    while True:

        # 1)If the frontier is empty, return failure.
        if frontier.isEmpty():
            return "Failure"
        # 2)Choose a leaf node and remove it from the frontier.
        node = frontier.pop()
        # 3)If the node returns a goal state, return the corresponding solution.
        if problem.isGoalState(node[0]):
            return node[1]
        # 4)Expand the chosen node, adding the resulting nodes to the frontier.
        if not node[0] in expandedNodes: #Check for the visited nodes
            expandedNodes.add(node[0])
            successors = problem.getSuccessors(node[0])

            for n in successors:
                path = list(node[1])
                path.append(n[1])
                frontier.push((n[0],path))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    #Frontier is a Priority Queue
    frontier = util.PriorityQueue()

    state = (problem.getStartState(), {})
    node = None
    expandedNodes = set()
    path = list()


    # Initialize the frontier using the initial state.
    # Frontier is based on the cost function.
    frontier.push(state, problem.getCostOfActions(state[1]))


    while True:
        # 1)If the frontier is empty, return failure.
        if frontier.isEmpty():
            return "Failure"
        # 2)Choose a leaf node and remove it from the frontier.
        node = frontier.pop()
        # 3)If the node returns a goal state, return the corresponding solution.
        if problem.isGoalState(node[0]):
            return node[1]
        # 4)Expand the chosen node, adding the resulting nodes to the frontier.
        if not node[0] in expandedNodes: #Check for the visited nodes
            expandedNodes.add(node[0])
            successors = problem.getSuccessors(node[0])

            for n in successors:
                path = list(node[1])
                path.append(n[1])
                frontier.push((n[0],path), problem.getCostOfActions(path))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    #Frontier is a Priority Queue
    frontier = util.PriorityQueue()

    state = (problem.getStartState(), {})
    node = None
    expandedNodes = set()
    path = list()

    # Initialize the frontier using the initial state.
    # Frontier is based on the sum of cost function and heuristic function.
    frontier.push(state, problem.getCostOfActions(state[1]) + heuristic(problem.getStartState(), problem))

    while True:
        # 1)If the frontier is empty, return failure.
        if frontier.isEmpty():
            return "Failure"
        # 2)Choose a leaf node and remove it from the frontier.
        node = frontier.pop()
        # 3)If the node returns a goal state, return the corresponding solution.
        if problem.isGoalState(node[0]):
            return node[1]
        # 4)Expand the chosen node, adding the resulting nodes to the frontier.
        if not node[0] in expandedNodes: #Check for the visited nodes
            expandedNodes.add(node[0])
            successors = problem.getSuccessors(node[0])

            for n in successors:
                path = list(node[1])
                path.append(n[1])
                frontier.push((n[0], path), problem.getCostOfActions(path) + heuristic(n[0], problem))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch