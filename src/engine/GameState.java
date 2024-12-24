package engine;

public class GameState {
	private static int NUM_COLUMNS = 7+2;
	private static int NUM_ROWS = 6+2;
	
	//adds padding to the sides of the classic 7x6 game board.
	private CellState [][] board = new CellState[NUM_COLUMNS][NUM_ROWS];
	
	//number of tokens in a given column
	private int[] columnTokenCount = new int[NUM_COLUMNS];
	
	//aka the current player
	private CellState nextTokenType= CellState.FIRST;
	
	public void reset() {
		for(int c=0;c<NUM_COLUMNS;++c)
			columnTokenCount[c]=0;
		for(int c=0;c<NUM_COLUMNS;++c)
			for(int r=0;r<NUM_ROWS;++r)
				board[c][r]=CellState.EMPTY;
		for(int c=0;c<NUM_COLUMNS;++c)
			board[c][0]=CellState.INVALID;
		for(int c=0;c<NUM_COLUMNS;++c)
			board[c][NUM_ROWS-1]=CellState.INVALID;
		for(int r=0;r<NUM_ROWS;++r)
			board[0][r]=CellState.INVALID;
		for(int r=0;r<NUM_ROWS;++r)
			board[NUM_COLUMNS-1][r]=CellState.INVALID;
		nextTokenType=CellState.FIRST;
	}
	
	/**
	 * shorthand for initializing the gamestate from move sequence.
	 * @param moveSeq
	 */
	public void set(String moveSeq) {
		reset();
		for (int i = 0; i < moveSeq.length(); i++) {
            char ch = moveSeq.charAt(i);
            int num = Character.getNumericValue(ch); // or (ch - '0')
            makeMove(num);
            assert false==is4Connected(num);
        }
	}
	
	/**
	 * Current player drops a token into the indicated column. Updates the game state.
	 * @param column
	 */
	public void makeMove(int column) {
		//todo: maybe this should check game win condition and return a flag for the current player?
		assert column>0 && column<NUM_COLUMNS;
		assert columnTokenCount[column]<NUM_ROWS-2;
		assert board[column][1+columnTokenCount[column]] == CellState.EMPTY;
		board[column][1+columnTokenCount[column]]=nextTokenType;
		columnTokenCount[column]+=1;
		nextTokenType = nextTokenType == CellState.FIRST ? CellState.SECOND : CellState.FIRST;
	}
	
	/**
	 * reverse of makeMove
	 * @param column
	 */
	public void unmakeMove(int column) {
		assert column>0 && column<NUM_COLUMNS;
		assert columnTokenCount[column]>0 && columnTokenCount[column]<NUM_ROWS-1;;
		assert board[column][columnTokenCount[column]] == CellState.FIRST || board[column][columnTokenCount[column]] == CellState.SECOND;
		board[column][columnTokenCount[column]]=CellState.EMPTY;
		columnTokenCount[column]-=1;
		nextTokenType = nextTokenType == CellState.FIRST ? CellState.SECOND : CellState.FIRST;
	}
	
	/**
	 * called after a move is made. searches all possible lines incorporating the last played token.
	 * @param lastUpdatedColumn
	 * @return
	 */
	public boolean is4Connected(int lastUpdatedColumn) {
		assert columnTokenCount[lastUpdatedColumn]>0 && columnTokenCount[lastUpdatedColumn]<NUM_ROWS-1;
		int lastUpdatedRow = columnTokenCount[lastUpdatedColumn];
		int numInSequence;
		CellState current, correctType;
		correctType = board[lastUpdatedColumn][lastUpdatedRow];
		assert correctType == CellState.FIRST || correctType == CellState.SECOND;
		int c, r;
		
		numInSequence=0;
		//horizontal
		{
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				r--;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				r++;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
		}
		if(numInSequence>=3)//not counting the starting point.
			return true;

		numInSequence=0;
		//vertical
		{
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c--;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c++;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
		}
		if(numInSequence>=3)//not counting the starting point.
			return true;
		
		numInSequence=0;
		//diagonal
		{
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c--;
				r--;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c++;
				r++;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
		}
		
		numInSequence=0;
		//other diagonal
		{
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c--;
				r++;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
			c=lastUpdatedColumn;
			r=lastUpdatedRow;
			do {
				c++;
				r--;
				current = board[c][r];
				if(current == correctType)
					numInSequence++;
				else
					break;
			}while(true);
		}
		if(numInSequence>=3)//not counting the starting point.
			return true;
		if(numInSequence>=3)//not counting the starting point.
			return true;
		
		
		return false;
	}
	
	public String toString() {
		String ret="";
		
		for(int c=1;c<NUM_COLUMNS-1;++c)
			ret+=" "+columnTokenCount[c];
		ret+="\n--------------\n";
		for(int r=NUM_ROWS-1;r>0;--r) {
			for(int c=1;c<NUM_COLUMNS-1;++c)
				if(board[c][r]==CellState.FIRST)
					ret+=" X";
				else if(board[c][r]==CellState.SECOND)
					ret+=" o";
				else
					ret+=" .";
			ret+="\n";
		}
		ret+="--------------\n";
		ret+= "Current Player: "+(nextTokenType==CellState.FIRST ? "first" : "second") + "\n";
		return ret;
	}
}
