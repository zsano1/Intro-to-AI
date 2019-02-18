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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        remaining food (newFood) and Pacman position after moving (newPos).
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
        "*** YOUR CODE HERE ***"
        ghost_state=[]
        food_dist=[]
        ghost_dist=[]
        for ghost in newGhostStates:
            ghost_state+=[ghost.getPosition()]
        if newPos in ghost_state and 0 in newScaredTimes:
            return -1
        if newPos in currentGameState.getFood().asList():
            return 1
        for i in range(len(newFood.asList())):
            food_dist.append(manhattanDistance(newFood.asList()[i],newPos))
        for j in range(len(ghost_state)):
            ghost_dist.append(manhattanDistance(ghost_state[j],newPos))
        return 1/min(food_dist)-1/min(ghost_dist)


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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def Max(state,d):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            next_state=[state.generateSuccessor(0,action) for action in state.getLegalActions(0)]
            temp=float("-inf")
            for n_s in next_state:
                temp=max(temp,Min(n_s,d,1))
            return temp
        def Min(state,d,agent_ind):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            next_state=[state.generateSuccessor(agent_ind,action) for action in state.getLegalActions(agent_ind)]
            temp=float("inf")
            for n_s in next_state:
                if agent_ind < gameState.getNumAgents()-1:
                    temp=min(temp,Min(n_s,d,agent_ind+1))
                else:
                    temp=min(temp,Max(n_s,d+1))
            return temp

        val = float("-inf")
        for action in gameState.getLegalActions():
          temp = Min(gameState.generateSuccessor(0,action), 0, 1)
          if temp > val:
            val = temp
            move = action
        return move

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def Max(state,d,alpha,beta):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            temp=float("-inf")
            for action in state.getLegalActions(0):
                temp=max(temp,Min(state.generateSuccessor(0,action),d,1,alpha,beta))
                if temp>beta:
                    return temp
                alpha=max(alpha,temp)
            return temp
        def Min(state,d,agent_ind,alpha,beta):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            temp=float("inf")
            for action in state.getLegalActions(agent_ind):
                if agent_ind==state.getNumAgents()-1:
                    temp=min(temp,Max(state.generateSuccessor(agent_ind,action),d+1,alpha,beta))
                else:
                    temp=min(temp,Min(state.generateSuccessor(agent_ind,action),d,agent_ind+1,alpha,beta))
                if temp<alpha:
                    return temp
                beta=min(beta,temp)
            return temp
        val=float("-inf")
        alpha=float("-inf")
        beta=float("inf")
        for action in gameState.getLegalActions(0):
            temp = Min(gameState.generateSuccessor(0,action), 0, 1,alpha,beta)
            if temp > val:
                val = temp
                move = action
                alpha=max(temp,alpha)
        return move
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
        def Max(state,d):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            temp=float("-inf")
            for action in state.getLegalActions(0):
                temp=max(temp,Exp(state.generateSuccessor(0,action),d,1))
            return temp
        def Exp(state,d,agent_ind):
            if state.isWin() or state.isLose() or d==self.depth:
                return self.evaluationFunction(state)
            temp=0
            if agent_ind == state.getNumAgents()-1:
                for action in state.getLegalActions(agent_ind):
                    temp+=Max(state.generateSuccessor(agent_ind,action),d+1)
            else:
                for action in state.getLegalActions(agent_ind):
                    temp+=Exp(state.generateSuccessor(agent_ind,action),d,agent_ind+1)
                temp/=len(state.getLegalActions(agent_ind))
            return temp
        val=float("-inf")

        for action in gameState.getLegalActions(0):
            temp = Exp(gameState.generateSuccessor(0,action), 0, 1)
            if temp > val:
                val = temp
                move = action
        return move

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <The return value contains four parts: the manhattan distance to the nearest food,
     the manhattan distance to the ghost, the surplus capsule and the current state getScore() score.>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    ghost_state = []
    food_dist = []
    ghost_dist = []
    for ghost in newGhostStates:
        ghost_state += [ghost.getPosition()]
    if newPos in ghost_state and 0 in newScaredTimes:
        return -1
    if newPos in currentGameState.getFood().asList():
        return 1
    for i in range(len(newFood.asList())):
        food_dist.append(manhattanDistance(newFood.asList()[i], newPos))
    for j in range(len(ghost_state)):
        ghost_dist.append(manhattanDistance(ghost_state[j], newPos))
    score=0
    if len(currentGameState.getCapsules()) < 2:
        score+=100
    min_food=0 if not food_dist else 1/min(food_dist)
    min_ghost=0 if not food_dist else 1/min(ghost_dist)
    score+=min_food*10+min_ghost+currentGameState.getScore()
    return score

better = betterEvaluationFunction
