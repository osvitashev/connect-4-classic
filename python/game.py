from GameState import GameState
from minimax_agent import MinimaxAgent

game = GameState()
agent = MinimaxAgent()

print(game.toDebugString())

while True:
    command = input("Enter your move [1..7] >> ")
    if command == "quit":
        break
    elif command == "switchside":
        agent.scoreLegalMoves(game)
        game.makeMove(agent.getBestMove())
        print(agent.getScoreReport())
        print(game.toDebugString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
    else:
        game.makeMove(int(command))
        print(game.toDebugString())
        print(game.toDebugString())
        if game.isVictory():
            print("WELL DONE!")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
        agent.scoreLegalMoves(game)
        print(agent.getScoreReport())
        game.makeMove(agent.getBestMove())
        print(game.toDebugString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
    
