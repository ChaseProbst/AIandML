# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

vecdic = {Directions.NORTH: (0, 1),
    Directions.SOUTH: (0, -1),
    Directions.EAST:  (1, 0),
    Directions.WEST:  (-1, 0),
    Directions.STOP:  (0, 0)}
directions = [Directions.EAST, Directions.SOUTH, Directions.WEST, Directions.NORTH, Directions.STOP]

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and
        Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newWalls = successorGameState.getWalls()
        #for i in range( len(newGhostStates) ):
        #    if newScaredTimes[]
        print "   "
        gain = 100
        for ghost in newGhostStates:
            if ( ghost.scaredTimer == 0 ):
                threatVector = tuple( map( lambda n1 , n2 : n1 - n2 , newPos, ghost.getPosition() ))
                print " ghost  : ", ghost
                print " threat : ", threatVector#, " info ", dir(ghost)
                for d in directions:
                    if threatVector == vecdic[d]:
                        gain -= 75
                        print " threating "
        # look down a hall way
        for dir in directions:
            for dist in range(2):
                squint = tuple( map( lambda n1 , n2 : n1 + dist * n2 , newPos , vecdic[dir] ))
                if newWalls[squint[0]][squint[1]]:
                    print "wall"
                    break
                elif newFood[squint[0]][squint[1]]:
                    print "smells good"
                    gain += 1
        # walk kinda towards food
        fgain = 0.0
        flist = newFood.asList()
        for fpos in flist:
            fgain += .9/manhattanDistance(fpos,newPos);
            #fgain = tuple( map( lambda fg, pp, fp : fg + abs( .1/ ( pp - fp )) , fgain, newPos, ghost.getPosition() ))
        print " fgain : ", fgain, " gain : ", gain
        #print "score :", successorGameState.getScore(), " at :", newPos, " food left : ", newFood.count()
        print "score : ", successorGameState.getScore(), " at : ", newPos
        # don't freeze
        if action == Directions.STOP:
            gain -= 10
        #dead end
        maddow = 0
        for dir in directions:
            squint = tuple( map( lambda n1 , n2 : n1 + n2 , newPos , vecdic[dir] ))
            if newWalls[squint[0]][squint[1]]:
                maddow +=1
        if maddow == 3:
            gain -= 5
        return successorGameState.getScore() + gain + fgain

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        from game import Directions
        from game import Actions
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.
        
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        validmoves  = gameState.getLegalActions(0)
        depth       = self.depth
        
        plunge = self.getToeAction( gameState, 0, 0)
        print " dipped :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth):
        #deafault
        #somedip = move , V
        bestDip = (Directions.STOP, 0)
        dip     = (Directions.STOP, 0)
        #                   bestdip returns a move and V
        if agent == 0:      bestDip = (Directions.STOP, -9999999);
        else:               bestDip = (Directions.STOP,  9999999);
        
        #end early or end of line
        if ( gameState.isWin() or gameState.isLose() or ( (toeDepth == self.depth) and ( agent == 0 ) ) ):
            return (Directions.STOP, self.evaluationFunction(gameState))
        
        #the real work
        moves = [move for move in gameState.getLegalActions(agent) if move != Directions.STOP]
        for move in moves:
            #increment
            nextGameState = gameState.generateSuccessor(agent,move);    nextAgent = agent + 1;  nextDip = toeDepth;
            
            #when you loop back to Pacman increase his toe's depth
            if nextAgent >= gameState.getNumAgents():   nextDip += 1;   nextAgent = 0;
            
            #peek
            dip = self.getToeAction(nextGameState, nextAgent, nextDip)
            
            # new best move
            if agent != 0 and dip[1] < bestDip[1]:
                bestDip = (move, dip[1])
            elif agent == 0 and dip[1] > bestDip[1]:
                bestDip = (move, dip[1])
                
        return bestDip

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #validmoves  = gameState.getLegalActions(0)
        #depth       = self.depth
        #print " agents ", gameState.getNumAgents(), " depth ",  self.depth , gameState.state
        plunge = self.getToeAction( gameState, 0, 1,-999999, 9999999)
        #print " Num agents ", gameState.getNumAgents(),
        print " plunge :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth, alpha, beta ):
        #default
        a = alpha; b = beta;
        # somedip  move, v
        bestV = [Directions.STOP, 0]
        laterV     = [Directions.STOP, 0]
        #                   bestdip returns a move and V
        if agent == 0:      bestV = [Directions.STOP, -99999];
        else:               bestV = [Directions.STOP,  99999];
        
        #end early or end of line
        if ( ( len(gameState.getLegalActions(agent)) == 0) or ( toeDepth == self.depth ) ):   #and ( agent == (gameState.getNumAgents() - 1) )) ):
            laterV = [Directions.STOP, self.evaluationFunction(gameState)]
            #print "< state: ", gameState.state, " $: ", laterV, " >" ,  gameState.getLegalActions(agent),
            #print "< baseCase: ", laterV, " f " ,  gameState.getLegalActions(agent), " >",
            return laterV
        
        #increment
        nextAgent = agent + 1;
        nextDepth = toeDepth;
        #when you loop back to Pacman increase his toe's depth
        if nextAgent >= ( gameState.getNumAgents() ):
            nextDepth = toeDepth + 1
            nextAgent = 0
        #print " state ", dir( gameState.state ),
        
        #the real work
        #moves = [move for move in gameState.getLegalActions(agent) ]
        for move in gameState.getLegalActions(agent):
        
            nextGameState = gameState.generateSuccessor(agent,move);
            
            #peek
            
            laterV = self.getToeAction(nextGameState, nextAgent, nextDepth, a, b)
            
            # new best move ops lol move is lost as implemented like the instruction
            if agent != 0 : #ghost min
                #print "<", gameState.state, " ", bestV, " ld ", laterV, " ", nextGameState.state, ">",
                #bestV[1] = min( bestV[1], laterV[1] ) # take min V as best
                if ( laterV[1] < bestV[1]  ):
                    bestV = [move, laterV[1]]
                if bestV[1] < a:  return [move, bestV[1]];
                #if laterV[1] < a:  return [laterV[0], laterV[1]]; peer sug
                b = min( b, bestV[1] );
                #bestV[0] = move
                
            elif agent == 0:
                #print "<", gameState.state, " ", bestV, " ld ", laterV, " ", nextGameState.state, " a: ", a, " b: ", b, ">",
                if ( laterV[1] > bestV[1] ):
                    bestV = [move, laterV[1]]
                #bestV[1] = max( bestV[1], laterV[1] )
                if bestV[1] > b:  return [ move, bestV[1] ];
                #if laterV[1] > b:  return [ laterV[0], laterV[1] ]; peer sug
                a = max( a, bestV[1] );
                #bestV[0] = move;
        
        return bestV
        
class AlphaBetaAgentPassAll(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #validmoves  = gameState.getLegalActions(0)
        #depth       = self.depth
        #print " agents ", gameState.getNumAgents(), " depth ",  self.depth , gameState.state
        plunge = self.getToeAction( gameState, 0, 0,-999999, 9999999)
        print " Num agents ", gameState.getNumAgents(),
        print " plunge :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth, alpha, beta ):
        #default
        a = alpha; b = beta;
        # somedip  move, v
        bestV = [Directions.STOP, 0]
        laterV     = [Directions.STOP, 0]
        #                   bestdip returns a move and V
        if agent == 0:      bestV = [Directions.STOP, -99999];
        else:               bestV = [Directions.STOP,  99999];
        
        #end early or end of line
        if ( (gameState.isWin() or gameState.isLose()) or ( toeDepth == self.depth ) ):   #and ( agent == (gameState.getNumAgents() - 1) )) ):
            return (Directions.STOP, self.evaluationFunction(gameState))
        
        #increment
        nextAgent = agent + 1;
        nextDepth = toeDepth +1;
        #when you loop back to Pacman increase his toe's depth
        if nextAgent >= ( gameState.getNumAgents() ):
            #nextDepth = toeDepth + 1
            nextAgent = 0
        #print " state ", dir( gameState.state ),
        
        #the real work
        #moves = [move for move in gameState.getLegalActions(agent) ]
        for move in gameState.getLegalActions(agent):
        
            nextGameState = gameState.generateSuccessor(agent,move);
            
            #peek
            
            laterV = self.getToeAction(nextGameState, nextAgent, nextDepth, a, b)
            
            # new best move ops lol move is lost as implemented like the instruction
            if agent != 0 : #ghost min
                print "<", gameState.state, " ", bestV, " ld ", laterV, " ", nextGameState.state, ">",
                #bestV[1] = min( bestV[1], laterV[1] ) # take min V as best
                if ( laterV[1] < bestV[1]  ):
                    bestV = [move, laterV[1]]
                if bestV[1] < a:  return [move, bestV[1]];
                #if laterV[1] < a:  return [laterV[0], laterV[1]]; peer sug
                b = min( b, bestV[1] );
                #bestV[0] = move
                
            elif agent == 0:
                print "<", gameState.state, " ", bestV, " ld ", laterV, " ", nextGameState.state, " a: ", a, " b: ", b, ">",
                if ( laterV[1] > bestV[1] ):
                    bestV = [move, laterV[1]]
                #bestV[1] = max( bestV[1], laterV[1] )
                if bestV[1] > b:  return [ move, bestV[1] ];
                #if laterV[1] > b:  return [ laterV[0], laterV[1] ]; peer sug
                a = max( a, bestV[1] );
                #bestV[0] = move;
        
        return bestV

class AlphaBetaAgentB3(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #validmoves  = gameState.getLegalActions(0)
        #depth       = self.depth
        print " agents ", gameState.getNumAgents(), " depth ",  self.depth , gameState.state
        plunge = self.getToeAction( gameState, 0, 0,-999999, 9999999)
        print " Num agents ", gameState.getNumAgents(),
        print " plunge :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth, alpha, beta ):
        #default
        a = alpha; b = beta;
        # somedip  move, v
        bestV = [Directions.STOP, 0]
        laterV     = [Directions.STOP, 0]
        #                   bestdip returns a move and V
        if agent == 0:      bestV = [Directions.STOP, alpha];
        else:               bestV = [Directions.STOP,  beta];
        
        #end early or end of line
        if ( gameState.isWin() or gameState.isLose() or ( toeDepth == self.depth ) ):   #and ( agent == (gameState.getNumAgents() - 1) )) ):
            return (Directions.STOP, self.evaluationFunction(gameState))
        
        #increment
        nextAgent = agent + 1;
        nextDepth = toeDepth +1;
        #when you loop back to Pacman increase his toe's depth
        if nextAgent >= ( gameState.getNumAgents() ):
            #nextDepth = toeDepth + 1
            nextAgent = 0
        #print " state ", dir( gameState.state ),
        
        #the real work
        #moves = [move for move in gameState.getLegalActions(agent) ]
        for move in gameState.getLegalActions(agent):
        
            nextGameState = gameState.generateSuccessor(agent,move);
            
            #peek
            
            laterV = self.getToeAction(nextGameState, nextAgent, nextDepth, a, b)
            
            # new best move ops lol move is lost as implemented like the instruction
            if agent != 0 : #ghost min
                bestV[1] = min( bestV[1], laterV[1] ) # take min V as best
                if bestV[1] < a:  return [move, bestV[1]];
                #if laterV[1] < a:  return [laterV[0], laterV[1]]; peer sug
                b = min( b, bestV[1] );
                #bestV[0] = move
                
            elif agent == 0:
                print "<cb ", bestV, " ld ", laterV, ">",
                bestV[1] = max( bestV[1], laterV[1] )
                if bestV[1] > b:  return [ move, bestV[1] ];
                #if laterV[1] > b:  return [ laterV[0], laterV[1] ]; peer sug
                a = max( a, bestV[1] );
                #bestV[0] = move;
        
        return bestV

class AlphaBetaAgentB2(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #validmoves  = gameState.getLegalActions(0)
        #depth       = self.depth
        
        plunge = self.getToeAction( gameState, 0, 0,-999999, 9999999)
        print " Num agents ", gameState.getNumAgents(),
        print " plunge :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth, alpha, beta ):
        #default
        a = alpha; b = beta;
        # somedip  move, v
        bestDip = [Directions.STOP, 0]
        laterDip     = [Directions.STOP, 0]
        #                   bestdip returns a move and V
        if agent == 0:      bestDip = [Directions.STOP, alpha];
        else:               bestDip = [Directions.STOP,  beta];
        
        #end early or end of line
        if ( gameState.isWin() or gameState.isLose() or ((toeDepth == self.depth) and ( agent == (gameState.getNumAgents() - 1) )) ):
            return (Directions.STOP, self.evaluationFunction(gameState))
        
        #increment
        nextAgent = agent + 1;
        nextDepth = toeDepth;
        #when you loop back to Pacman increase his toe's depth
        if nextAgent >= gameState.getNumAgents():
            nextDepth = toeDepth + 1
            nextAgent = 0
        
        #the real work
        moves = [move for move in gameState.getLegalActions(agent) ]
        for move in moves:
        
            nextGameState = gameState.generateSuccessor(agent,move);
            
            #peek
            laterDip = self.getToeAction(nextGameState, nextAgent, nextDepth, a, b)
            
            # new best move ops lol move is lost as implemented like the instruction
            if agent != 0 : #ghost min
                bestDip[1] = min( bestDip[1], laterDip[1] ) # take min V as best
                if bestDip[1] < a:  #print " depth ", toeDepth, " where ", [move, bestDip[1]],
                    return [move, bestDip[1]]
                b = min( b, bestDip[1] )
                bestDip[0] = move;
            elif agent == 0:
                bestDip[1] = max( bestDip[1], laterDip[1] )
                if bestDip[1] > b:  #print " depth ", toeDepth, " where ", [move, bestDip[1]],
                    return [ move, bestDip[1] ]
                a = max(a, bestDip[1]);
                bestDip[0] = move;
        #print " depth ", toeDepth, " where ", [bestDip[0], bestDip[1]],
        return bestDip
        
    #def max_V()


class AlphaBetaAgentBackup(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        validmoves  = gameState.getLegalActions(0)
        depth       = self.depth
        
        plunge = self.getToeAction( gameState, 0, 0,-999999, 9999999)
        print " dipped :", plunge
        return plunge[0]
        
        
    def getToeActionB(self, gameState, agent, toeDepth, alpha, beta ):
            #deafault
        bestDip = (Directions.STOP, 0)
        dip     = (Directions.STOP, 0)
        if agent == 0:
            bestDip = (Directions.STOP, alpha, beta) # max - pacman
        else:
            bestDip = (Directions.STOP, alpha, beta) #  min - ghost
        
            #end early or end of line
        if ( gameState.isWin() or gameState.isLose() ):
            if( agent == 0 ):
                return (Directions.STOP, self.evaluationFunction(gameState), beta) # maxing
            else:
                return (Directions.STOP, alpha, self.evaluationFunction(gameState)) # minning
            #cut off
        if ( (toeDepth == self.depth) and ( agent == 0 ) ):
            print " broke "
            return (Directions.STOP, self.evaluationFunction(gameState), self.evaluationFunction(gameState), beta)
        
        #the real work
        moves = [move for move in gameState.getLegalActions(agent) if move != Directions.STOP]
        for move in moves:
            print " hit ",
            #increment
            
            nextGameState = gameState.generateSuccessor(agent,move)
            nextAgent = agent + 1
            nextDip = toeDepth
            #when you loop back to Pacman increase his toe's depth
            if nextAgent >= gameState.getNumAgents():
                nextDip += 1
                nextAgent = 0
                
            #peek
            if(agent != 0  ):
                dip = self.getToeAction( nextGameState, nextAgent, nextDip, bestDip[1], bestDip[2]) #min
                if( dip[1] < bestDip[2] ):
                    bestDip = (move, bestDip[2], dip[1])
                    print "| min ", bestDip, " | ",
            else:
                dip = self.getToeAction( nextGameState, nextAgent, nextDip, bestDip[1], bestDip[2])#max
                #if max dip beats beta then break as this max node wont be chosen
                if ( dip[1] > bestDip[2] ):# maybe check to see if this is at its deepest
                    bestDip = (move, dip[1], dip[2])
                    print "| max b", bestDip, " | ",
                    break
                elif ( dip[1] > bestDip[1] ): # if dip a is higher then a replace it.
                    bestDip = (move, dip[1], dip[2])
                    print "| max ", bestDip, " | ",
                
            #break if better options come about
            #if ( agent == gameState.getNumAgents() -1 ) and ( dip[2] > bestDip[1]) :      #min prunning
            #    bestDip = (move, alphaBeta, dip[1])
            #    print "| min b", bestDip, " | ",
            #    break
            #elif agent == 0 and dip[1] < bestDip[2]:    #max
            #    bestDip = (move, dip[1], alphaBeta)
            #    print "| max b", bestDip, " | ",
            #    break
                
            # new best move
            #if agent != 0 and dip[2] < bestDip[2]:      # minning
            #    bestDip = (move, bestDip[2], dip[1])
            #    print "| min ", bestDip, " | ",
            #elif agent == 0 and dip[1] > bestDip[1]:    # maxing
            #    bestDip = (move, dip[1], bestDip[2])
            #    print "| max ", bestDip, " | ",
        return bestDip
        
    def getToeActionbackup(self, gameState, agent, toeDepth, alphaBeta ):
        #deafault
        bestDip = (Directions.STOP, 0)
        dip     = (Directions.STOP, 0)
        if agent == 0:
            bestDip = (Directions.STOP, -9999999, alphaBeta) # max - pacman
        else:
            bestDip = (Directions.STOP, alphaBeta, 9999999) #  min - ghost
        
        #end early or end of line
        if ( gameState.isWin() or gameState.isLose() ):
            if( agent == 0 ):
                return (Directions.STOP, self.evaluationFunction(gameState), alphaBeta) # maxing
            else:
                return (Directions.STOP, alphaBeta, self.evaluationFunction(gameState)) # minning
        #cut off
        if ( (toeDepth == self.depth) and ( agent == 0 ) ):
            print " broke "
            return (Directions.STOP, self.evaluationFunction(gameState), alphaBeta)
        
        #the real work
        moves = [move for move in gameState.getLegalActions(agent) if move != Directions.STOP]
        for move in moves:
            print " hit ",
            #increment
            
            nextGameState = gameState.generateSuccessor(agent,move)
            nextAgent = agent + 1
            nextDip = toeDepth
            #when you loop back to Pacman increase his toe's depth
            if nextAgent >= gameState.getNumAgents():
                nextDip += 1
                nextAgent = 0
                
            #peek
            if(agent != 0  ):
                dip = self.getToeAction( nextGameState, nextAgent, nextDip, bestDip[1]) #min
                if( dip[1] < bestDip[2] ):
                    bestDip = (move, bestDip[2], dip[1])
                    print "| min ", bestDip, " | ",
            else:
                dip = self.getToeAction( nextGameState, nextAgent, nextDip, bestDip[2])#max
                #if max dip beats beta then break as this max node wont be chosen
                if ( dip[1] > bestDip[2] ):# maybe check to see if this is at its deepest
                    bestDip = (move, dip[1], dip[2])
                    print "| max b", bestDip, " | ",
                    break
                elif ( dip[1] > bestDip[1] ): # if dip a is higher then a replace it.
                    bestDip = (move, dip[1], dip[2])
                    print "| max ", bestDip, " | ",
                
            #break if better options come about
            #if ( agent == gameState.getNumAgents() -1 ) and ( dip[2] > bestDip[1]) :      #min prunning
            #    bestDip = (move, alphaBeta, dip[1])
            #    print "| min b", bestDip, " | ",
            #    break
            #elif agent == 0 and dip[1] < bestDip[2]:    #max
            #    bestDip = (move, dip[1], alphaBeta)
            #    print "| max b", bestDip, " | ",
            #    break
                
            # new best move
            #if agent != 0 and dip[2] < bestDip[2]:      # minning
            #    bestDip = (move, bestDip[2], dip[1])
            #    print "| min ", bestDip, " | ",
            #elif agent == 0 and dip[1] > bestDip[1]:    # maxing
            #    bestDip = (move, dip[1], bestDip[2])
            #    print "| max ", bestDip, " | ",
        return bestDip
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #validmoves  = gameState.getLegalActions(0)
        #depth       = self.depth
        
        plunge = self.getToeAction( gameState, 0, 0)
        print " dipped :", plunge
        return plunge[0]
        
    #origally I started with a dipping your toe in type analong it kinda fell apart tho
    def getToeAction(self, gameState, agent, toeDepth):
        #deafault
        #somedip = move , V
        bestDip = (Directions.STOP, 0)
        dip     = (Directions.STOP, 0)
        #                   bestdip returns a move and V
        if agent == 0:      bestDip = (Directions.STOP, -9999999);
        else:               bestDip = (Directions.STOP,  9999999);
        
        #print dir( gameState )
        #end early or end of line
        if ( gameState.isWin() or gameState.isLose() or ( (toeDepth == self.depth) and ( agent == 0 ) ) ):
            return (Directions.STOP, self.evaluationFunction(gameState))
        
        #increment
        nextAgent = agent + 1;  nextDip = toeDepth;
        #when you loop back to Pacman increase his toe's depth
        if nextAgent >= gameState.getNumAgents():   nextDip += 1;   nextAgent = 0;
        
        
        min_avg = 0
        #the real work
        moves = [move for move in gameState.getLegalActions(agent)]
        for move in moves:
            
            
            #peek
            nextGameState = gameState.generateSuccessor(agent,move);
            dip = self.getToeAction(nextGameState, nextAgent, nextDip)
            
            # new best move
            if agent != 0:# and dip[1] < bestDip[1]:
                #bestDip = (move, dip[1])
                min_avg += dip[1]
            elif agent != 0 and dip[1] < bestDip[1]:
                bestDip[0] = move
            elif agent == 0 and dip[1] > bestDip[1]:
                bestDip = (move, dip[1])
        if agent != 0:
            bestDip = ( bestDip[0],  min_avg/len(moves) )
        return bestDip

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I Basic got the vaild moves from the current game state      then    looped them through a copy of my p1 eval function       then        took the avg of them
      The if else does nothing it used to but I phased that out and I got a 4/6 so I just don't want to break anything
    """
    "*** YOUR CODE HERE ***"
    print "  ", dir (currentGameState)
    if ( currentGameState.getFood().count() >= 5 ):
        sum = 0.0
        moves = [move for move in currentGameState.getLegalActions(0)] #if move != Directions.STOP]
        for move in moves:
            sum += subBetterEvaluationFunction(currentGameState, move)
        if len(moves) == 0:
            if currentGameState.isWin():
                return 1000
            else:
                return 0
        return ( sum/len(moves))
    else:
        sum = 0.0
        moves = [move for move in currentGameState.getLegalActions(0)] #if move != Directions.STOP]
        for move in moves:
            sum += subBetterEvaluationFunction(currentGameState, move)
            #sum += hungryEvalFunction(currentGameState, move)
        if len(moves) == 0:
            if currentGameState.isWin():
                return 1000
            else:
                return 0
        return ( sum/len(moves))
    
def subBetterEvaluationFunction( currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and
    Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newTokens = successorGameState.getCapsules()
    #print " ", dir( successorGameState )
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newWalls = successorGameState.getWalls()
    #for i in range( len(newGhostStates) ):
    #    if newScaredTimes[]
    print "   "
    gain = 100
    for ghost in newGhostStates:
        if ( ghost.scaredTimer == 0 ):
            threatVector = tuple( map( lambda n1 , n2 : n1 - n2 , newPos, ghost.getPosition() ))
            print " ghost  : ", ghost
            print " threat : ", threatVector#, " info ", dir(ghost)
            for d in directions:
                if threatVector == vecdic[d]:
                    gain -= 75
                    print " threating "
    # look down a hall way
    for dir in directions:
        for dist in range(2):
            squint = tuple( map( lambda n1 , n2 : n1 + dist * n2 , newPos , vecdic[dir] ))
            if newWalls[squint[0]][squint[1]]:
                print "wall"
                break
            elif newFood[squint[0]][squint[1]]:
                print "smells good"
                gain += 1
    # walk kinda towards food
    fgain = 0.0
    flist = newFood.asList()
    for fpos in flist:
        fgain += .9/manhattanDistance(fpos,newPos);
        if (flist == currentGameState.getPacmanPosition ):
            fgain += 20
        if (flist == successorGameState.getPacmanPosition ):
            fgain += 20
    
        #fgain = tuple( map( lambda fg, pp, fp : fg + abs( .1/ ( pp - fp )) , fgain, newPos, ghost.getPosition() ))
    
    #walk kinda towards token
    tgain = 0.0
    #tlist = newTokens.asList()
    for tpos in newTokens:
        temp = manhattanDistance(tpos,newPos);
        if manhattanDistance < 2:
            tgain = 30
    
    
    # don't freeze
    if action == Directions.STOP:
        gain -= 10
    #dead end
    maddow = 0
    for dir in directions:
        squint = tuple( map( lambda n1 , n2 : n1 + n2 , newPos , vecdic[dir] ))
        if newWalls[squint[0]][squint[1]]:
            maddow +=1
    if maddow == 3:
        gain -= 5
        
        
    #print " fgain : ", fgain, " gain : ", gain , " tgain : ", tgain
    #print "score :", successorGameState.getScore(), " at :", newPos, " food left : ", newFood.count()
    #print "score : ", successorGameState.getScore(), " at : ", newPos
    
    return successorGameState.getScore() + gain + fgain *10 + tgain
def hungryEvalFunction( currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and
    Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newTokens = successorGameState.getCapsules()
    #print " ", dir( successorGameState )
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newWalls = successorGameState.getWalls()
    #for i in range( len(newGhostStates) ):
    #    if newScaredTimes[]
    print "   "
    gain = 100
    for ghost in newGhostStates:
        if ( ghost.scaredTimer == 0 ):
            threatVector = tuple( map( lambda n1 , n2 : n1 - n2 , newPos, ghost.getPosition() ))
            print " ghost  : ", ghost
            print " threat : ", threatVector#, " info ", dir(ghost)
            for d in directions:
                if threatVector == vecdic[d]:
                    gain -= 75
                    print " threating "
    """
    # look down a hall way
    for dir in directions:
        for dist in range(2):
            squint = tuple( map( lambda n1 , n2 : n1 + dist * n2 , newPos , vecdic[dir] ))
            if newWalls[squint[0]][squint[1]]:
                print "wall"
                break
            elif newFood[squint[0]][squint[1]]:
                print "smells good"
                gain += 1
    # walk kinda towards food
    fgain = 0.0
    flist = newFood.asList()
    for fpos in flist:
        fgain += .9/manhattanDistance(fpos,newPos);
        #fgain = tuple( map( lambda fg, pp, fp : fg + abs( .1/ ( pp - fp )) , fgain, newPos, ghost.getPosition() ))

    #walk kinda towards token
    tgain = 0.0
    #tlist = newTokens.asList()
    for tpos in newTokens:
        temp = manhattanDistance(tpos,newPos);
        if manhattanDistance < 2:
            tgain = 30


    # don't freeze
    if action == Directions.STOP:
        gain -= 10
    #dead end
    maddow = 0
    for dir in directions:
        squint = tuple( map( lambda n1 , n2 : n1 + n2 , newPos , vecdic[dir] ))
        if newWalls[squint[0]][squint[1]]:
            maddow +=1
    if maddow == 3:
        gain -= 5
        
        
    #print " fgain : ", fgain, " gain : ", gain , " tgain : ", tgain
    #print "score :", successorGameState.getScore(), " at :", newPos, " food left : ", newFood.count()
    #print "score : ", successorGameState.getScore(), " at : ", newPos
    """
    fgain = 0.0
    flist = newFood.asList()
    for fpos in flist:
        fgain += .9/manhattanDistance(fpos,newPos)
        if fpos == currentGameState.getPacmanPosition():
            fgain += 100
    return gain + fgain

# Abbreviation
better = betterEvaluationFunction

