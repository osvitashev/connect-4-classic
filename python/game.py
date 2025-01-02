from GameState import GameState
from BasicAlphaBetaAgent import BasicAlphaBetaAgent
import time

def calculate_ebf(total_nodes, depth, tolerance=1e-6):
    if depth <= 0:
        raise ValueError("Depth must be greater than 0")
    if total_nodes <= 0:
        raise ValueError("Total nodes must be greater than 0")
    low, high = 1, total_nodes
    while high - low > tolerance:
        mid = (low + high) / 2
        estimated_nodes = sum(mid**i for i in range(depth + 1))
        if estimated_nodes < total_nodes:
            low = mid
        else:
            high = mid
    return (low + high) / 2

def getNextAIMove(g, a):
    start = time.perf_counter()
    move = a.getBestMove(g)
    end = time.perf_counter()
    print(f"Depth: {a.getSearchDepth()}. Execution time: {end - start:.3f} seconds. Node count: {a.getNodeCount()} nodes. Speed: {(0.001*a.getNodeCount()/(end - start)):.1f}k nodes per second. Effective Branching Factor: {calculate_ebf(a.getNodeCount(), a.getSearchDepth()):.3f}.")
    print(f"Best Move = {move}")
    return move

game = GameState()
agent = BasicAlphaBetaAgent()
agent.setSearchDepth(11)

print(game.toDebugString())

while True:
    command = input("Enter your move [1..7] >> ")
    if command == "quit" or command == "stop" or command == "exit":
        break
    elif command == "switchside":
        game.makeMove(getNextAIMove(game, agent))
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
        game.makeMove(getNextAIMove(game, agent))
        print(game.toDebugString())
        if game.isVictory():
            print("AI WINS! Try again...")
            break
        elif game.isDraw():
            print("A draw... better luck next time.")
            break
    
