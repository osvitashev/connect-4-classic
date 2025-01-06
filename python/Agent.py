from GameState import GameState
import time

class Agent:

    def __init__(self):
        self._searchDepth = 0
        self._timeAllowed_ms = 0
        self._transpositionTable = {}
        """
        this is maintained as a part of internal state of the agent.
        does not carry over between searches - gets reset together with nodeCount.
        This means that each new search will be centered at the 0 regardless of the game state.
        This also means that the score does not need to be updated externally when the other player updates game state.
        
        """
        self._incrementalScore =0
        self._reset()
        
    def getScore(self):
        return self._incrementalScore
    
    def setSearchDepth(self, sd):
        self._searchDepth = sd
        
    def getSearchDepth(self):
        return self._searchDepth
    
    def _reset(self):
        self._transpositionTable = {}
        self._nodeCount = 1
        self._incrementalScore =0
    
    def getNodeCount(self):
        return self._nodeCount
    
    def getBestMove(self, g):
        self._reset()
        if g.isVictory() or g.isDraw():
            raise ValueError("Game cannot be continued")
        score, bestMove = self._alphaBeta(g, -self._VICTORY_SCORE, self._VICTORY_SCORE, 1)
        # print(f"Best Move = {bestMove}, score={score}")
        return bestMove
    
    def getGoodMove(self, g):
        self._reset()
        raise ValueError("NOT IMPLEMENTED!")
    
    def evaluateAllAndGetBestMove(self, g):
        raise ValueError("NOT IMPLEMENTED!")
    
    def _alphaBeta(self, g, alpha, beta, depth):
        print("NOT IMPLEMENTED")
