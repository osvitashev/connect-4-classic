from GameState import GameState
from minimax_agent import MinimaxAgent
game = GameState()

game.makeMove(3)
game.makeMove(4)
game.makeMove(3)
game.makeMove(4)
game.makeMove(3)
game.makeMove(4)

print(game.toDebugString())

agent = MinimaxAgent()
agent.scoreLegalMoves(game)
print(agent.getScoreReport())