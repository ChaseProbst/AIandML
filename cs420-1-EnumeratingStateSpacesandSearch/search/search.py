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

stk = util.Stack()
hist = {}

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
    from game import Directions
    from game import Actions
    #defaults
    adjnodes = problem.getSuccessors(problem.getStartState())
    move = Directions.STOP
    pman = problem.getStartState()
    won = problem.isGoalState(problem.getStartState())
    
    print "Start:", problem.getStartState()
    #print "Start type:", type(problem.getStartState())
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Is the start goal type?", type(problem.isGoalState(problem.getStartState()))
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    limit = 15
    moves = []
    while won == False:
        #setup
        adjnodes = problem.getSuccessors(pman)
        
        
        #hist is the 'paint' 0 none, 1 visted, 2 complete
        
        if pman in hist: # for avoiding visted nodes or backing out
            iscomplete = len(adjnodes)
            for node in adjnodes:
                if node[0] in hist:
                    iscomplete -= 1
            if iscomplete == 0:
                hist[pman] = 2
                prev = stk.pop()
                lastm = moves.pop()
                #moves.append( Actions.vectorToDirection((next[0]-pman[0],next[1]-pman[1]))  )
                #pman = (top[0]-lastm[0],top[1]-lastm[0])
                pman = prev
                won = problem.isGoalState(pman)
                print "popped ", pman
                continue
        else:
            hist[pman] = 1
        
        #next move
        
        next = adjnodes[0]
        bestpaint = 2
        
        for node in adjnodes:
            #print "    For ", node[0]
            #print "hist :", hist
            if node[0] in hist:
                #print "in hist ", node[0]
                if bestpaint > hist[node[0]]:
                    bestpaint = hist[node[0]]
                    next = node
                #print "hit deep A"
            elif bestpaint != 0 :
                bestpaint = 0
                next = node
                #print "hit", node
        
        stk.push(pman)
        moves.append(next[1])
        pman = next[0]
        #print "Next's successors:", problem.getSuccessors(pman)
        """if limit == 0:
            won = True
        limit = limit -1"""
        won = problem.isGoalState(pman)
        #if (True == problem.isGoalState(problem.getStartState())):
        #moves.append( Directions.STOP)
    print "win ", pman
    print "win moves ", moves
    return moves



def breadthFirstSearch(problem):
    from game import Directions
    from game import Actions
    #defaults
    adjnodes = problem.getSuccessors(problem.getStartState()) # frontier
    pman = problem.getStartState()
    move = (0,[])
    won = False
    que = util.Queue() # explored w/ data of node 
    #moves = []
    #cost = 0
    rcd = { pman : (1,0,[]) } # [ (x,y) : ( paint, cost, [path] ) ]
    
    # o setup
    que.push(pman)
    
    #traversal
    while won == False:
        if que.isEmpty():
            for x in rcd: print x
        pman = que.pop()
        adjnodes = problem.getSuccessors(pman)
        move = ( problem.getCostOfActions(rcd[pman][2]) , rcd[pman][2] )
        for node in adjnodes:
            if not node[0] in rcd:
                rcd[node[0]] = (1, move[0] + node[2], move[1] + [node[1]] )
                que.push(node[0])
        
        won = problem.isGoalState(pman)

    return rcd[pman][2]



def uniformCostSearch(problem):
    from game import Directions
    from game import Actions
    #defaults
    adjnodes = problem.getSuccessors(problem.getStartState())
    pman = problem.getStartState()
    move = (0,[])
    won = False
    que = util.PriorityQueueWithFunction(problem.costFn)
    #moves = []
    #cost = 0
    rcd = { pman : (1,0,[]) } # [ (x,y) : ( paint, cost, [path] ) ]
    
    # o setup
    que.push(pman)
    
    #traversal
    while won == False:
        if que.isEmpty():
            for x in rcd: print x
        pman = que.pop()
        adjnodes = problem.getSuccessors(pman)
        move = ( rcd[pman][1] , rcd[pman][2] )
        for node in adjnodes:
            if not node[0] in rcd:
                rcd[node[0]] = (1, move[0] + node[2], move[1] + [node[1]] )
                que.push(node[0])
        
        won = problem.isGoalState(pman)
    return rcd[pman][2]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def curryHeuristic( s, h ):
    def f( gn, state, problem):
        return s( gn, h( state, problem ) )
    return f
def sumhelp(a,b):
    return a + b

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from game import Directions
    from game import Actions
    #defaults
    adjnodes = problem.getSuccessors(problem.getStartState())
    pman = problem.getStartState()
    move = (0,[])
    won = False
    #print problem.costFn
    que = util.PriorityQueueWithFunctionAndCustomPush(curryHeuristic(sumhelp, heuristic))
    #moves = []
    #cost = 0
    rcd = { pman : (1,0,[]) } # [ (x,y) : ( paint, cost, [path] ) ]
    
    # o setup
    que.push(pman, 0, problem)
    
    #traversal
    while won == False:
        if que.isEmpty():
            for x in rcd: print x
        pman = que.pop()
        adjnodes = problem.getSuccessors(pman)
        move = ( rcd[pman][1] , rcd[pman][2] )
        for node in adjnodes:
            if not node[0] in rcd:
                rcd[node[0]] = (1, move[0] + node[2], move[1] + [node[1]] )
                que.push( node[0], move[0] + node[2], problem)
        
        won = problem.isGoalState(pman)
    
    return rcd[pman][2]

def breadthFirstSearchbackup(problem):
    from game import Directions
    from game import Actions
    #defaults
    adjnodes = problem.getSuccessors(problem.getStartState())
    pman = problem.getStartState()
    move = (pman, (0,0,[Directions.STOP]))
    won = problem.isGoalState(problem.getStartState())
    que = util.Queue()
    moves = []
    cost = 0
    rcd = {} # [ (x,y) : ( paint, cost, [path] ) ]
    
    # o setup
    que.push(pman)
    #traversal
    """while won == false:
        for node in adjnodes:
        if node[0] in rcd:
        if rcd[node[0]][1] < (cost + node[2]):
        
        won = problem.isGoalState(pman)
        """
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
