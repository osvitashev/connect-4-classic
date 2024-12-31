from GameState import GameState
from AgentV1 import BasicAlphaBetaAgent



def playGame(agent1, agent2):
    global wins, draws, losses, game, challenger, defender
    while True:
        game.makeMove(agent1.getBestMove(game))
        if game.isDraw():
            draws+=1
            break
        elif game.isVictory() and  agent1 == challenger:
            wins+=1
            break
        elif game.isVictory() and  agent1 == defender:
            losses +=1
            break
        game.makeMove(agent2.getBestMove(game))
        if game.isDraw():
            draws+=1
            break
        elif game.isVictory() and  agent1 == challenger:
            wins+=1
            break
        elif game.isVictory() and  agent1 == defender:
            losses +=1
            break


##from challenger's perspective
wins = 0
draws = 0
losses =0

challenger = BasicAlphaBetaAgent(8)
defender = BasicAlphaBetaAgent(6)



for m1 in [1,2,3,4,5,6,7]:
    for m2 in [1,2,3,4,5,6,7]:
        for m3 in [1,2,3,4,5,6,7]:
            game=GameState()
            game.makeMove(m1)
            game.makeMove(m2)
            game.makeMove(m3)
            playGame(challenger, defender)
            print(f"Report>>> wins:{wins}, draws:{draws}, losses:{losses}")
            game=GameState()
            game.makeMove(m1)
            game.makeMove(m2)
            game.makeMove(m3)
            playGame(defender, challenger)
            print(f"Report>>> wins:{wins}, draws:{draws}, losses:{losses}")


print(f"Report>>> wins:{wins}, draws:{draws}, losses:{losses}")
print(f"Advantage: {(wins-losses)/(wins+losses):.2f}")

