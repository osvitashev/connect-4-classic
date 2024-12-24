package agent.minimax;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

import engine.GameState;

class TestBAsicSearch {

	@Test
	void test() {
		MinimaxAgent agent = new MinimaxAgent();
		GameState g = new GameState();
		g.set("454545");
		System.out.println(g.toString());
		agent.pickNextMove(g);
		System.out.println(agent.getScoreByColumnReport());
		
		g.set("454545533");
		System.out.println(g.toString());
		agent.pickNextMove(g);
		System.out.println(agent.getScoreByColumnReport());

		
	}

}
