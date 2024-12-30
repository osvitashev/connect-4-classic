from GameState import GameState
from AgentV1 import BasicAlphaBetaAgent

game = GameState()
agent = BasicAlphaBetaAgent(9)

print(game.toDebugString())

while True:
    command = input("Enter your move [1..7] >> ")
    if command == "quit" or command == "stop" or command == "exit":
        break
    elif command == "switchside":
        game.makeMove(agent.evaluateAllAndGetBestMove(game))
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
        if game.isVictory():
            print("WELL DONE!")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
        game.makeMove(agent.evaluateAllAndGetBestMove(game))
        print(game.toDebugString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
    
