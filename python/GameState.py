from CellState import CellState

class GameState:
    NUM_COLUMNS = 7 + 2
    NUM_ROWS = 6 + 2

    # Constructor
    def __init__(self):        
        self._firstPlayerTokens = 0
        self._secondPlayerTokens = 0
        """
        list of (col, row) pairs
        """
        self._game_history = []
        
        self._columnTokenCount = [0] * GameState.NUM_COLUMNS
        # # AKA the current player
        self._nextTokenType = CellState.FIRST
        self._numTokensPlayed = 0
        self._victoryFlag = False
    
    def getLastUpdatedCellCoordinates(self):
        """
        returns pair (col, row)
        """
        return self._game_history[-1]
    
    def getFirstPlayerTokens(self):
        return self._firstPlayerTokens
    
    def getSecondPlayerTokens(self):
        return self._secondPlayerTokens
            
    def getBitIndex(c, r):
        return c+GameState.NUM_COLUMNS*r
    
    def _getCellValue(self, c, r):
        if c == 0 or c == GameState.NUM_COLUMNS-1 or r == 0 or r == GameState.NUM_ROWS-1:
            return CellState.INVALID
        elif 0 != self._firstPlayerTokens & (1 << GameState.getBitIndex(c, r)):
            return CellState.FIRST
        elif 0 != self._secondPlayerTokens & (1 << GameState.getBitIndex(c, r)):
            return CellState.SECOND
        else:
            return CellState.EMPTY
        
        return self._board[c][r]
    
    def _setCellValue(self, c, r, value):
        if value == CellState.FIRST:
            self._firstPlayerTokens = self._firstPlayerTokens | (1 << GameState.getBitIndex(c, r))
        else:
            self._secondPlayerTokens = self._secondPlayerTokens | (1 << GameState.getBitIndex(c, r))
    
    def _clearCellValue(self, c, r):
        self._firstPlayerTokens = self._firstPlayerTokens & ~(1 << GameState.getBitIndex(c, r))
        self._secondPlayerTokens = self._secondPlayerTokens & ~(1 << GameState.getBitIndex(c, r))
            
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
            assert self._getCellValue(column, 1 + self._columnTokenCount[column]) == CellState.EMPTY
            assert self._victoryFlag == False
        self._setCellValue(column, 1 + self._columnTokenCount[column], self._nextTokenType)
        self._columnTokenCount[column] += 1
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed += 1
        self._victoryFlag = self._is4Connected(column)
        self._game_history.append((column, self._columnTokenCount[column]))
    
    def unmakeMove(self, column):
        if __debug__:
            assert column > 0 and column < GameState.NUM_COLUMNS - 1
            assert self._columnTokenCount[column] > 0 and self._columnTokenCount[column] < GameState.NUM_ROWS - 1
            assert self._getCellValue(column, self._columnTokenCount[column]) == CellState.FIRST or self._getCellValue(column, self._columnTokenCount[column]) == CellState.SECOND
        self._clearCellValue(column, self._columnTokenCount[column])
        self._columnTokenCount[column] -= 1;
        if self._nextTokenType == CellState.FIRST:
            self._nextTokenType = CellState.SECOND
        else:
            self._nextTokenType = CellState.FIRST
        self._numTokensPlayed -= 1
        self._victoryFlag = False
        self._game_history.pop()
            
    def _is4Connected(self, last_updated_column):
        if __debug__:
            assert self._columnTokenCount[last_updated_column] > 0 and self._columnTokenCount[last_updated_column] < self.NUM_ROWS - 1
        last_updated_row = self._columnTokenCount[last_updated_column]
        correct_type = self._getCellValue(last_updated_column,last_updated_row)
        if __debug__:
            assert correct_type == CellState.FIRST or correct_type == CellState.SECOND
        
        num_in_sequence = 0
# horizontal
        c = last_updated_column
        r = last_updated_row
        while True:
            r -= 1
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            r += 1
            current = self._getCellValue(c,r)
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
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            current = self._getCellValue(c,r)
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
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            r += 1
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        if num_in_sequence >= 3:  # not counting the starting point.
            return True
        
        num_in_sequence = 0
        # other diagonal
        c = last_updated_column
        r = last_updated_row
        while True:
            c -= 1
            r += 1
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        c = last_updated_column
        r = last_updated_row
        while True:
            c += 1
            r -= 1
            current = self._getCellValue(c,r)
            if current == correct_type:
                num_in_sequence += 1
            else:
                break
        
        if num_in_sequence >= 3:  # not counting the starting point.
            return True
        return False
    
    def getMoveHistoryString(self):
        return ''.join(str(pair[0]) for pair in self._game_history)
    
    def toDisplayString(self):
        ret = ""
        ret += "gameHist: "
        ret += ''.join(str(pair[0]) for pair in self._game_history)
        ret += "\n"
        ret += "--------------\n";
        for r in reversed(range(1, GameState.NUM_ROWS - 1)):
            for c in range(1, GameState.NUM_COLUMNS - 1):
                ret += " " + self._getCellValue(c,r).value
            ret += "\n"
        ret += "--------------\n";
        ret += "-1-2-3-4-5-6-7\n";
        ret += "Current Player: " + self._nextTokenType.value
        return ret
    
    def toDebugString(self):
        ret = "=================\n"
        ret += f"numTokensPlayed: {self._numTokensPlayed}\n"
        ret += f"columnTokenCount: {self._columnTokenCount}\n"
        ret += f"victoryFlag: {self._victoryFlag}\n"
        ret += self.toDisplayString()
        return ret
    
    def isMoveValid(self, column):
        if __debug__:
            assert column >= 1 and column < GameState.NUM_COLUMNS - 1
        return self._getCellValue(column,1 + self._columnTokenCount[column]) == CellState.EMPTY
