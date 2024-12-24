package play;

import java.util.Scanner;

import agent.minimax.MinimaxAgent;
import engine.GameState;

public class Game {

	static GameState game=new GameState();
	static MinimaxAgent agent = new MinimaxAgent();
	
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		game.reset();
				
		Scanner scanner = new Scanner(System.in);
		String input;
		while(true) {
			System.out.println(game.toString());
			System.out.println("Enter your move [1..7]");
			input=scanner.nextLine();
			if(input.equals("exit"))
				break;
			else if(input.equals("newgame")) {
				game.reset();
			}
			else if(input.equals("newgame player=first")) {
				game.reset();
				game.makeMove(agent.pickNextMove(game));
				System.out.println(agent.getScoreByColumnReport());
			}
			else {
				int col = Integer.valueOf(input);
				game.makeMove(col);
				game.makeMove(agent.pickNextMove(game));
				System.out.println(agent.getScoreByColumnReport());
			}
			
			
			
		}
		
		scanner.close();
		
	}

}
