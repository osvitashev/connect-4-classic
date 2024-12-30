from GameState import GameState
from Agent import Agent


class BasicAlphaBetaAgent(Agent):
    _VICTORY_SCORE = 50
    _COLUMNS_IN_TRAVERSAL_ORDER = [4,3,5,2,6,1,7]#{1, 2, 3, 4, 5, 6, 7}
    
    # Constructor
    # def __init__(self):
    
    def evaluateAllAndGetBestMove(self, g):
        """
        Does not do beta-cuts on the first iteration - this results in redundancy,
        but gives exact score for every available move. Useful for testing.
        """
        self._nodeCount = 1
        assert not g.isVictory()
        assert not g.isDraw()
        scoreByColumn = [0] * GameState.NUM_COLUMNS
        
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            score = -self._VICTORY_SCORE
            if g.isMoveValid(column):
                g.makeMove(column)
                if g.isVictory():
                    score = self._VICTORY_SCORE - 1
                else:
                    score = -self._alphaBeta(g, -self._VICTORY_SCORE, self._VICTORY_SCORE, 2)
                g.unmakeMove(column)
            scoreByColumn[column] = score
        rep = ""
        for c in range(1, GameState.NUM_COLUMNS - 1):
            rep += f"{c}->{scoreByColumn[c]} "
        # print(f"Score by Column: {rep}")
        bestScore = -self._VICTORY_SCORE
        bestMove = -1
        for c in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if scoreByColumn[c] > bestScore:
                bestScore = scoreByColumn[c]
                bestMove = c
        # print(f">>>>>>>>>>>AI's move: {bestMove}")
        return bestMove
    
    def _alphaBeta(self, g, alpha, beta, depth):
        if __debug__:
            self._nodeCount += 1
        if depth > self._searchDepth or g.isDraw():
            return 0
        score = 0
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                if g.isVictory():
                    score = self._VICTORY_SCORE - depth
                else:
                    score = -self._alphaBeta(g, -beta, -alpha, depth + 1)
                g.unmakeMove(column)
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

