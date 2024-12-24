package agent.minimax;

import engine.GameState;

public class MinimaxAgent {
	static final int MAX_SEARCH_DEPTH = 12;
	
	//for the purposes if a/b search, this is the positive and negative infinity.
	static final int VICTORY_SCORE = 100;
	
	static final int[] COLUMNS_IN_TRAVERSAL_ORDER = {1,2,3,4,5,6,7};
	
	//for tracing purposes only
	private int[] scoreByColumn = new int[7+2];
	
	/**
	 * 
	 * @param g
	 * @return column for next suggested move [1..7], or -1 if there are no legal moves available. (board is full, it is a draw.)
	 */
	public int pickNextMove(GameState g) {
		int currentScore=-VICTORY_SCORE;
		int currentMove = -1;
		int score;
		for(int i=0;i<COLUMNS_IN_TRAVERSAL_ORDER.length;++i) {
			int column=COLUMNS_IN_TRAVERSAL_ORDER[i];
			if(g.isMoveValid(column)) {
				g.makeMove(column);
				if(g.is4Connected(column))
					score=VICTORY_SCORE-1;
				else
					score = -alphaBeta(g,-VICTORY_SCORE,VICTORY_SCORE, 2);
				if(score>currentScore) {
					currentScore=score;
					currentMove=column;
				}
				g.unmakeMove(column);
				scoreByColumn[column]=score;
//				System.out.println("Column="+column+"; score="+score);
			}
		}
		return currentMove;
	}
	
	/**
	 * performs recusive negamax search with enhancements.
	 * @return anticipated score of the current position
	 */
	private int alphaBeta(GameState g, int alpha, int beta, int depth) {
		if(depth>=MAX_SEARCH_DEPTH)
			return 0;//draw score
		int score;
		for(int i=0;i<COLUMNS_IN_TRAVERSAL_ORDER.length;++i) {
			int column=COLUMNS_IN_TRAVERSAL_ORDER[i];
			if(g.isMoveValid(column)) {
				g.makeMove(column);
				if(g.is4Connected(column))
					score=VICTORY_SCORE-depth;
				else
					score = -alphaBeta(g,-beta, -alpha, depth+1);
				g.unmakeMove(column);
				
				if( score >= beta )
			         return beta;   //  fail hard beta-cutoff
			      if( score > alpha )
			         alpha = score; // alpha acts like max in MiniMax
			}
		}
		
		return alpha;
	}
	
	public String getScoreByColumnReport() {
		String s="";
		for(int c=1;c<=7;++c)
			s+="Column="+c+"; score="+scoreByColumn[c]+"\n";
		return s;
	}
}
