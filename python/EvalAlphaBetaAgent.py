from Agent import Agent
from GameState import GameState

def cond(depth):
#         if depth >= 1 and depth <=11:
#             return True
#         else:
    return False

class EvalAlphaBetaAgent(Agent):
    _VICTORY_SCORE = 1000
    _COLUMNS_IN_TRAVERSAL_ORDER = [4,3,5,2,6,1,7]#{1, 2, 3, 4, 5, 6, 7}
    
    _POSITIONAL_SCORE = [
    0,0,0,0,0,0,0,0,0,
    0, 3, 4, 5, 7, 5, 4, 3, 0,
    0, 4, 6, 8, 10, 8, 6, 4, 0,
    0, 5, 8, 10, 12, 10, 8, 5, 0,
    0, 5, 8, 10, 12, 10, 8, 5, 0,
    0, 4, 6, 8, 10, 8, 6, 4, 0,
    0, 3, 4, 5, 7, 5, 4, 3, 0, 
    0,0,0,0,0,0,0,0,0
]
    
    # Constructor
    # def __init__(self):
    
    def _updateScoreAfterMakeMove(self, game):
        col = game.getLastUpdatedCellCoordinates()[0]
        row = game.getLastUpdatedCellCoordinates()[1]
        scoreChange = EvalAlphaBetaAgent._POSITIONAL_SCORE[GameState.getBitIndex(col, row)]
        self._incrementalScore += scoreChange
        self._incrementalScore = -self._incrementalScore
        
    def _updateScoreBeforeUnmakeMove(self, game):
        col = game.getLastUpdatedCellCoordinates()[0]
        row = game.getLastUpdatedCellCoordinates()[1]
        scoreChange = EvalAlphaBetaAgent._POSITIONAL_SCORE[GameState.getBitIndex(col, row)]
        self._incrementalScore = -self._incrementalScore
        self._incrementalScore -= scoreChange
        
    
    
    def _alphaBeta(self, g, alpha, beta, depth):
        if g.isDraw():
            return 0, None
        if depth > self._searchDepth:
            return self._incrementalScore, None
        score = None
        bestMove = None
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                self._updateScoreAfterMakeMove(g)
                self._nodeCount += 1
                if g.isVictory():
                    score = self._VICTORY_SCORE - depth
                else:
                    if cond(depth) and (g.getFirstPlayerTokens(), g.getSecondPlayerTokens()) in self._transpositionTable:
                        score = self._transpositionTable[(g.getFirstPlayerTokens(), g.getSecondPlayerTokens())]
                    else:
                        score, move = self._alphaBeta(g, -beta, -alpha, depth + 1)
                        score = -score
                        if cond(depth):
                            self._transpositionTable[(g.getFirstPlayerTokens(), g.getSecondPlayerTokens())]=score
                        # print(g.getMoveHistoryString() + " score: " + str(score))
                        
                self._updateScoreBeforeUnmakeMove(g)
                g.unmakeMove(column)
                
                if score >= beta:
                    return beta, None
                if score > alpha:
                    alpha = score
                    bestMove = column
        return alpha, bestMove

