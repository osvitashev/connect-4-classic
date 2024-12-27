package engine;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class TestGameState {

	@Test
	void testBasicActions() {
		GameState game = new GameState();
		game.reset();

//		System.out.println(game.toString());

		assertEquals(" 0 0 0 0 0 0 0\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ "--------------\n"
				+ "Current Player: first\n", game.toString());

		game.makeMove(3);
		assertEquals(" 0 0 1 0 0 0 0\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . X . . . .\n"
				+ "--------------\n"
				+ "Current Player: second\n", game.toString());

		game.makeMove(3);
		assertEquals(" 0 0 2 0 0 0 0\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . o . . . .\n"
				+ " . . X . . . .\n"
				+ "--------------\n"
				+ "Current Player: first\n", game.toString());

		game.makeMove(7);
		assertEquals(" 0 0 2 0 0 0 1\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . o . . . .\n"
				+ " . . X . . . X\n"
				+ "--------------\n"
				+ "Current Player: second\n", game.toString());
		
		game.makeMove(2);
		game.makeMove(4);
		game.makeMove(4);
		game.makeMove(5);
		assertFalse(game.is4Connected(5));
		game.makeMove(5);
		assertFalse(game.is4Connected(5));
		
		game.makeMove(6);
		assertTrue(game.is4Connected(6));
		assertEquals(" 0 1 2 2 2 1 1\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . o o o . .\n"
				+ " . o X X X X X\n"
				+ "--------------\n"
				+ "Current Player: second\n", game.toString());
		
		game.unmakeMove(6);
		assertEquals(" 0 1 2 2 2 0 1\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . o o o . .\n"
				+ " . o X X X . X\n"
				+ "--------------\n"
				+ "Current Player: first\n", game.toString());
		
//		System.out.println(game.toString());
		
		game.reset();
		assertEquals(" 0 0 0 0 0 0 0\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ "--------------\n"
				+ "Current Player: first\n", game.toString());
		
//		System.out.println(game.toString());
	}// test case
	
	@Test
	void testWinDetection() {
		GameState g = new GameState();
		g.set("121212");
		assertEquals(" 3 3 0 0 0 0 0\n"
				+ "--------------\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " . . . . . . .\n"
				+ " X o . . . . .\n"
				+ " X o . . . . .\n"
				+ " X o . . . . .\n"
				+ "--------------\n"
				+ "Current Player: first\n", g.toString());
		//test vertical
		g.makeMove(1);
		assertTrue(g.is4Connected(1));
		g.unmakeMove(1);
		g.makeMove(3);
		g.makeMove(2);
		assertTrue(g.is4Connected(2));
		g.unmakeMove(2);
		
		g.makeMove(1);
		g.makeMove(2);
		g.makeMove(3);
		g.makeMove(1);
		g.makeMove(4);
		//test diagonal
//		System.out.println(g.toString());
		assertTrue(g.is4Connected(4));
		g.unmakeMove(4);
		
		g.makeMove(5);
		g.makeMove(4);
		g.makeMove(5);
		g.makeMove(3);
		
		g.makeMove(4);
		//test horizontal
//		System.out.println(g.toString());
		assertTrue(g.is4Connected(4));
		g.unmakeMove(4);
		
		g.set("6565544441");
		g.makeMove(7);
		//test diagonal
		assertTrue(g.is4Connected(7));
		g.unmakeMove(7);
		
		
//		System.out.println(g.toString());
	}
}
