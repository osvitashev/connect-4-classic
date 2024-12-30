from GameState import GameState
from AgentV1 import BasicAlphaBetaAgent
import time

def calculate_ebf(total_nodes, depth, tolerance=1e-6):
    if depth <= 0:
        raise ValueError("Depth must be greater than 0")
    if total_nodes <= 0:
        raise ValueError("Total nodes must be greater than 0")
    low, high = 1, total_nodes  # EBF is at least 1 and at most the total nodes
    while high - low > tolerance:
        mid = (low + high) / 2
        # Compute the number of nodes with the current b*
        estimated_nodes = sum(mid**i for i in range(depth + 1))
        if estimated_nodes < total_nodes:
            low = mid  # Increase b*
        else:
            high = mid  # Decrease b*
    return (low + high) / 2

depth = 10

game = GameState()
agent = BasicAlphaBetaAgent(depth)

start = time.perf_counter()
# Code to time
agent.evaluateAllAndGetBestMove(game)
end = time.perf_counter()

print(f"Startpos search depth: {depth}. Execution time: {end - start:.6f} seconds. Node count: {agent.getNodeCount()} nodes. Speed: {(0.001*agent.getNodeCount()/(end - start)):.1f} k nodes per second. Effective Branching Factor: {calculate_ebf(agent.getNodeCount(), depth):.3f}.")
