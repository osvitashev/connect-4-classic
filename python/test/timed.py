from GameState import GameState
from AgentV1 import BasicAlphaBetaAgent
import time

game = GameState()
agent = BasicAlphaBetaAgent(0)

start = time.perf_counter()
if -1 == agent.getBestMoveOnTimer(game, 5000):
    print("foobar")
end = time.perf_counter()

print(f"Execution time: {end - start:.6f} seconds.")
