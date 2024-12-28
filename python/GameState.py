from CellState import CellState


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
        assert column > 0 and column < GameState.NUM_COLUMNS-1
        assert self.isMoveValid(column)
        assert self._board[column][1 + self._columnTokenCount[column]] == CellState.EMPTY
        assert self._victoryFlag == False
        self._board[column][1 + self._columnTokenCount[column]] = self._nextTokenType
        self._columnTokenCount[column] += 1
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed+=1
        self._victoryFlag = self._is4Connected(column)
    
    def unmakeMove(self, column):
        assert column > 0 and column < GameState.NUM_COLUMNS-1
        assert self._columnTokenCount[column]>0 and self._columnTokenCount[column]<GameState.NUM_ROWS-1
        assert self._board[column][self._columnTokenCount[column]] == CellState.FIRST or self._board[column][self._columnTokenCount[column]] == CellState.SECOND
        self._board[column][self._columnTokenCount[column]]=CellState.EMPTY;
        self._columnTokenCount[column]-=1;
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed-=1
        self._victoryFlag = False

            
    def _is4Connected(self, last_updated_column):
        assert self._columnTokenCount[last_updated_column] > 0 and self._columnTokenCount[last_updated_column] < self.NUM_ROWS - 1
        last_updated_row = self._columnTokenCount[last_updated_column]
        correct_type = self._board[last_updated_column][last_updated_row]
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
    
    def toDebugString(self):
        ret = "=================\n"
        ret+= f"numTokensPlayed: {self._numTokensPlayed}\n"
        ret+= f"columnTokenCount: {self._columnTokenCount}\n"
        ret+= f"victoryFlag: {self._victoryFlag}\n"
        ret+=self.toDisplayString()
        return ret
    
    def isMoveValid(self, column):
        assert column >= 1 and column < GameState.NUM_COLUMNS - 1
        return self._board[column][1 + self._columnTokenCount[column]] == CellState.EMPTY
