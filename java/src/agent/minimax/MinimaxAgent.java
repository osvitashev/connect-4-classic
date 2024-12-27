package agent.minimax;

import java.util.Random;

import engine.GameState;

public class MinimaxAgent {
	static final int MAX_SEARCH_DEPTH = 9;

	// for the purposes if a/b search, this is the positive and negative infinity.
	static final int VICTORY_SCORE = 100;

	static final int[] COLUMNS_IN_TRAVERSAL_ORDER = {1,2,3,4,5,6,7};

	// for tracing purposes only
	private int[] scoreByColumn = new int[7 + 2];

	Random random = new Random();

	public int pickNextMove(GameState g) {
		scoreLegalMoves(g);
		int numPositiveScores = 0, numZeroScores = 0;
		for (int c = 1; c < GameState.NUM_COLUMNS - 1; ++c) {
			if (scoreByColumn[c] > 0)
				numPositiveScores++;
			else if (scoreByColumn[c] == 0)
				numZeroScores++;
		}
		if (numPositiveScores > 0) {
			int i=0, reti = random.nextInt(numPositiveScores);
			for (int c = 1; c < GameState.NUM_COLUMNS - 1; ++c)
				if(scoreByColumn[c]>0)
					if(i==reti)
						return c;
					else
						i++;
		} else if (numZeroScores > 0) {
			int i=0, reti = random.nextInt(numZeroScores);
			for (int c = 1; c < GameState.NUM_COLUMNS - 1; ++c)
				if(scoreByColumn[c]==0)
					if(i==reti)
						return c;
					else
						i++;
		} else {
			int currentScore = Integer.MIN_VALUE;
			int currentIndex = 0;
			for (int c = 1; c < GameState.NUM_COLUMNS - 1; ++c) {
				if (scoreByColumn[c] > currentScore) {
					currentScore = scoreByColumn[c];
					currentIndex = c;
				}
			}
			return currentIndex;
		}
		return -2;//should not be reachable.
	}

	private void scoreLegalMoves(GameState g) {
		int score;
		for (int i = 0; i < COLUMNS_IN_TRAVERSAL_ORDER.length; ++i) {
			score = -VICTORY_SCORE;
			int column = COLUMNS_IN_TRAVERSAL_ORDER[i];
			if (g.isMoveValid(column)) {
				g.makeMove(column);
				if (g.is4Connected(column))
					score = VICTORY_SCORE - 1;
				else
					score = -alphaBeta(g, -VICTORY_SCORE, VICTORY_SCORE, 2);
				g.unmakeMove(column);
			}
			scoreByColumn[column] = score;
		}
		System.out.println(getScoreByColumnReport());
	}

	/**
	 * performs recusive negamax search with enhancements.
	 * 
	 * @return anticipated score of the current position
	 */
	private int alphaBeta(GameState g, int alpha, int beta, int depth) {
		if (depth >= MAX_SEARCH_DEPTH)
			return 0;// draw score
		int score;
		for (int i = 0; i < COLUMNS_IN_TRAVERSAL_ORDER.length; ++i) {
			int column = COLUMNS_IN_TRAVERSAL_ORDER[i];
			if (g.isMoveValid(column)) {
				g.makeMove(column);
				if (g.is4Connected(column))
					score = VICTORY_SCORE - depth;
				else
					score = -alphaBeta(g, -beta, -alpha, depth + 1);
				g.unmakeMove(column);

//				if (score >= beta)
//					return beta; // fail hard beta-cutoff
				if (score > alpha)
					alpha = score; // alpha acts like max in MiniMax
			}
		}

		return alpha;
	}

	public String getScoreByColumnReport() {
		String s = "";
		for (int c = 1; c <= 7; ++c)
			s += "Column=" + c + "; score=" + scoreByColumn[c] + "\n";
		return s;
	}
}
