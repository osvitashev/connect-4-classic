from GameState import GameState
import time

class Agent:

    def __init__(self):
        self._searchDepth = 0
        self._timeAllowed_ms = 0
        self._reset()
    
    def setSearchDepth(self, sd):
        self._searchDepth = sd
        
    def getSearchDepth(self):
        return self._searchDepth
    
    def _reset(self):
        self._nodeCount = 1
    
    def getNodeCount(self):
        return self._nodeCount
    
    def getBestMove(self, g):
        self._reset()
        if g.isVictory() or g.isDraw():
            raise ValueError("Game cannot be continued")
        score, bestMove = self._alphaBeta(g, -self._VICTORY_SCORE, self._VICTORY_SCORE, 1)
        # print(f"Best Move = {bestMove}")
        return bestMove
    
    def getGoodMove(self, g):
        self._reset()
        raise ValueError("NOT IMPLEMENTED!")
    
    def evaluateAllAndGetBestMove(self, g):
        raise ValueError("NOT IMPLEMENTED!")
    
    def _alphaBeta(self, g, alpha, beta, depth):
        print("NOT IMPLEMENTED")
