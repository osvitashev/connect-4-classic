from GameState import GameState
import time

class Agent:

    def __init__(self, searchDepth):
        self._searchDepth = searchDepth
        self._timeAllowed_ms = 0
        self._reset()
    
    def _reset(self):
        self._nodeCount = 1
    
    def getNodeCount(self):
        return self._nodeCount
    
    def getBestMoveOnTimer(self, g, timems):
        depth = 6
        ret = -1
        self._timeAllowed_ms = timems
        start = time.perf_counter()
        while True:
            self._searchDepth = depth
            ret = self.getBestMove(g)
            end = time.perf_counter()
            print(f"Searched depth = {depth}, Execution time: {end - start:.3f} seconds.")
            if (end-start) > self._timeAllowed_ms / 3: # 3x2 as the estimated branching factor plus second conversion
                break
            else :
                depth += 1
        end = time.perf_counter()
        if(1000*(end-start)>timems):
            print("Calculation went over time limit!!!")
        #     raise AssertionError("Calculation went over time!")
        return ret
    
    def getBestMove(self, g):
        self._reset()
        if g.isVictory() or g.isDraw():
            raise ValueError("Game cannot be continued")
        score = 0
        bestMove = -1
        alpha = -self._VICTORY_SCORE
        beta = self._VICTORY_SCORE
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                if g.isVictory():
                    score = self._VICTORY_SCORE - 1
                else:
                    score = -self._alphaBeta(g, -beta, -alpha, 2)
                g.unmakeMove(column)
                if score > alpha:
                    alpha = score
                    bestMove = column
        return bestMove
    
    def getGoodMove(self, g):
        self._reset()
        raise ValueError("NOT IMPLEMENTED!")
    
    def evaluateAllAndGetBestMove(self, g):
        """
        Does not do beta-cuts on the first iteration - this results in redundancy,
        but gives exact score for every available move. Useful for testing.
        """
        self._reset()
        if g.isVictory() or g.isDraw():
            raise ValueError("Game cannot be continued")
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
        print("NOT IMPLEMENTED")
