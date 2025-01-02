from GameState import GameState
from Agent import Agent
from pip._vendor.pyparsing import col


class BasicAlphaBetaAgent(Agent):
    _VICTORY_SCORE = 50
    _COLUMNS_IN_TRAVERSAL_ORDER = [4,3,5,2,6,1,7]#{1, 2, 3, 4, 5, 6, 7}
    
    # Constructor
    # def __init__(self):

    
    def _alphaBeta(self, g, alpha, beta, depth):
        if depth > self._searchDepth or g.isDraw():
            return 0, None
        score = None
        bestMove = None
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                self._nodeCount += 1
                if g.isVictory():
                    score = self._VICTORY_SCORE - depth
                else:
                    score, move = self._alphaBeta(g, -beta, -alpha, depth + 1)
                    score = -score
                g.unmakeMove(column)
                if score >= beta:
                    return beta, None
                if score > alpha:
                    alpha = score
                    bestMove = column
        return alpha, bestMove

