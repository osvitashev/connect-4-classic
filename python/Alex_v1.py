from enum import Enum
import time

class CellState(Enum):
    INVALID = "INVALID"
    EMPTY = "."
    FIRST = "X"
    SECOND = "o"

def calculate_ebf(total_nodes, depth, tolerance=1e-6):
    if depth <= 0:
        raise ValueError("Depth must be greater than 0")
    if total_nodes <= 0:
        raise ValueError("Total nodes must be greater than 0")
    low, high = 1, total_nodes
    while high - low > tolerance:
        mid = (low + high) / 2
        estimated_nodes = sum(mid**i for i in range(depth + 1))
        if estimated_nodes < total_nodes:
            low = mid
        else:
            high = mid
    return (low + high) / 2

class GameState:
    NUM_COLUMNS = 7 + 2
    NUM_ROWS = 6 + 2

    # Constructor
    def __init__(self):
        self._board = [[CellState.EMPTY for _ in range(GameState.NUM_ROWS)] for _ in range(GameState.NUM_COLUMNS)]
        self._columnTokenCount = [0] * GameState.NUM_COLUMNS
        # # AKA the current player
        self._nextTokenType = CellState.FIRST
        self._numTokensPlayed = 0
        self._victoryFlag = False
        for c in range(0, GameState.NUM_COLUMNS):
            self._board[c][0] = CellState.INVALID
            self._board[c][GameState.NUM_ROWS - 1] = CellState.INVALID
        for r in range(0, GameState.NUM_ROWS):
            self._board[0][r] = CellState.INVALID
            self._board[GameState.NUM_COLUMNS - 1][r] = CellState.INVALID
            
    def isVictory(self):
        return self._victoryFlag
    
    def isDraw(self):
        return 42 == self._numTokensPlayed
    
    def setup(self, moveSeq):
        for c in [int(char) for char in moveSeq]:
            self.makeMove(c)
            assert False == self._is4Connected(c)
    
    def makeMove(self, column):
        if __debug__:
            assert column > 0 and column < GameState.NUM_COLUMNS - 1
            assert self.isMoveValid(column)
            assert self._board[column][1 + self._columnTokenCount[column]] == CellState.EMPTY
            assert self._victoryFlag == False
        self._board[column][1 + self._columnTokenCount[column]] = self._nextTokenType
        self._columnTokenCount[column] += 1
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed += 1
        self._victoryFlag = self._is4Connected(column)
    
    def unmakeMove(self, column):
        if __debug__:
            assert column > 0 and column < GameState.NUM_COLUMNS - 1
            assert self._columnTokenCount[column] > 0 and self._columnTokenCount[column] < GameState.NUM_ROWS - 1
            assert self._board[column][self._columnTokenCount[column]] == CellState.FIRST or self._board[column][self._columnTokenCount[column]] == CellState.SECOND
        self._board[column][self._columnTokenCount[column]] = CellState.EMPTY;
        self._columnTokenCount[column] -= 1;
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed -= 1
        self._victoryFlag = False
            
    def _is4Connected(self, last_updated_column):
        if __debug__:
            assert self._columnTokenCount[last_updated_column] > 0 and self._columnTokenCount[last_updated_column] < self.NUM_ROWS - 1
        last_updated_row = self._columnTokenCount[last_updated_column]
        correct_type = self._board[last_updated_column][last_updated_row]
        if __debug__:
            assert correct_type == CellState.FIRST or correct_type == CellState.SECOND;
        
        num_in_sequence = 0
# horizontal
        c = last_updated_column
        r = last_updated_row
        while True:
            r -= 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            r += 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        if num_in_sequence >= 3:  # not counting the starting point.
            return True
        
        num_in_sequence = 0
        # vertical
        c = last_updated_column
        r = last_updated_row
        while True:
            c -= 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        if num_in_sequence >= 3:  # not counting the starting point.
            return True
        
        num_in_sequence = 0
        # diagonal
        c = last_updated_column
        r = last_updated_row
        while True:
            c -= 1
            r -= 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            r += 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        num_in_sequence = 0
        # other diagonal
        c = last_updated_column
        r = last_updated_row
        while True:
            c -= 1
            r += 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            r -= 1
            current = self._board[c][r]
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        if num_in_sequence >= 3:  # not counting the starting point.
            return True
        return False
    
    def toDisplayString(self):
        ret = ""
        ret += "--------------\n";
        for r in reversed(range(1, GameState.NUM_ROWS - 1)):
            for c in range(1, GameState.NUM_COLUMNS - 1):
                ret += " " + self._board[c][r].value
            ret += "\n"
        ret += "--------------\n";
        ret += "-1-2-3-4-5-6-7\n";
        ret += "Current Player: " + self._nextTokenType.value
        return ret
    
    def isMoveValid(self, column):
        if __debug__:
            assert column >= 1 and column < GameState.NUM_COLUMNS - 1
        return self._board[column][1 + self._columnTokenCount[column]] == CellState.EMPTY

class Agent:
    _VICTORY_SCORE = 50
    _COLUMNS_IN_TRAVERSAL_ORDER = [4,3,5,2,6,1,7]#{1, 2, 3, 4, 5, 6, 7}
    
    def __init__(self):
        self._searchDepth = 0
        self._timeAllowed_ms = 0
        self._reset()
    
    def setSearchDepth(self, sd):
        self._searchDepth = sd
    
    def _reset(self):
        self._nodeCount = 1
    
    def getNodeCount(self):
        return self._nodeCount
    
    def getBestMove(self, g):
        self._reset()
        if g.isVictory() or g.isDraw():
            raise ValueError("Game cannot be continued")
        start = time.perf_counter()
        
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
        end = time.perf_counter()
        print(f"Search depth: {self._searchDepth}. Execution time: {end - start:.3f} seconds. Node count: {agent.getNodeCount()} nodes. Speed: {(0.001*agent.getNodeCount()/(end - start)):.1f}k nodes per second. Effective Branching Factor: {calculate_ebf(self.getNodeCount(), self._searchDepth):.3f}.")
        print(f"Best Move = {bestMove}")
        return bestMove

    
    def _alphaBeta(self, g, alpha, beta, depth):
        if depth > self._searchDepth or g.isDraw():
            return 0
        score = 0
        for column in self._COLUMNS_IN_TRAVERSAL_ORDER:
            if g.isMoveValid(column):
                g.makeMove(column)
                self._nodeCount += 1
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

game = GameState()
agent = Agent()
agent.setSearchDepth(11)

print(game.toDisplayString())

while True:
    command = input("Enter your move [1..7] >> ")
    if command == "quit" or command == "stop" or command == "exit":
        break
    elif command == "switchside":
        game.makeMove(agent.getBestMove(game))
        print(game.toDisplayString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
    else:
        game.makeMove(int(command))
        print(game.toDisplayString())
        if game.isVictory():
            print("WELL DONE!")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
        game.makeMove(agent.getBestMove(game))
        print(game.toDisplayString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
