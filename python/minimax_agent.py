from GameState import GameState
class MinimaxAgent:
    MAX_SEARCH_DEPTH = 7
    VICTORY_SCORE = 50
    COLUMNS_IN_TRAVERSAL_ORDER = {1,2,3,4,5,6,7}
    
    # Constructor
    def __init__(self):
        self._scoreByColumn = [0] * GameState.NUM_COLUMNS
    
    def getScoreReport(self):
        ret = ""
        for c in range(1, GameState.NUM_COLUMNS - 1):
            ret+=f"{c}->{self._scoreByColumn[c]} "
        return ret
    
    def scoreLegalMoves(self, g):
        assert not g.isVictory()
        assert not g.isDraw()
        for column in self.COLUMNS_IN_TRAVERSAL_ORDER:
            score=-self.VICTORY_SCORE
            if g.isMoveValid(column):
                g.makeMove(column)
                if g.isVictory():
                    score = self.VICTORY_SCORE-1
                else:
                    score = -self.alphaBeta(g, -self.VICTORY_SCORE, self.VICTORY_SCORE, 2)
                g.unmakeMove(column)
            self._scoreByColumn[column] = score
    
    def alphaBeta(self, g, alpha, beta, depth):
        if depth >=self.MAX_SEARCH_DEPTH or g.isDraw():
            return 0
        score =0
        for column in self.COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                if g.isVictory():
                    score = self.VICTORY_SCORE-depth
                else:
                    score = -self.alphaBeta(g, -beta, -alpha, depth + 1)
                g.unmakeMove(column)
                if score >= beta:
                    return beta
                if score>alpha:
                    alpha=score
        return alpha















