from BasicAlphaBetaAgent import BasicAlphaBetaAgent
from GameState import GameState
import time
from BasicAlphaBetaAgent_NO_TRANSPOSE import BasicAlphaBetaAgent_NO_TRANSPOSE
"""
The version with transpose plays #1 after 1534444443335335555676226
the version without transpose plays #2

Seems to be only happening with depth=4
"""


def getNextAIMove(g, a):
    start = time.perf_counter()
    move = a.getBestMove(g)
    end = time.perf_counter()
    print(f"Depth: {a.getSearchDepth()}. Execution time: {end - start:.3f} seconds. Node count: {a.getNodeCount()} nodes. Speed: {(0.001*a.getNodeCount()/(end - start)):.1f}k nodes per second.")
    return move

agent = BasicAlphaBetaAgent_NO_TRANSPOSE()
agent.setSearchDepth(4)
game=GameState()

startpos = "1534444443335335555676226"

game.setup(startpos)

print(startpos + "...")
game.makeMove(getNextAIMove(game, agent))
print(game.toDebugString())




# agent = BasicAlphaBetaAgent_NO_TRANSPOSE()
# agent.setSearchDepth(4)
# game=GameState()
#
# game.setup("1534444443335335555676226")
#
# game.makeMove(getNextAIMove(game, agent))
# print(game.toDebugString())













