import unittest
from GameState import GameState  # Replace 'your_module' with the actual module name

class TestMathOperations(unittest.TestCase):

    def test_basic_operations(self):
        game = GameState();
        
        self.assertEqual(game.toDisplayString(), """--------------
 . . . . . . .
 . . . . . . .
 . . . . . . .
 . . . . . . .
 . . . . . . .
 . . . . . . .
--------------
-1-2-3-4-5-6-7
Current Player: X""")
        
        self.assertEqual(game.isMoveValid(1), True)
        
        game.setup("12121221212")
        # print(game.toDisplayString())
        self.assertEqual(game.isMoveValid(1), True)
        self.assertEqual(game.isMoveValid(2), False)
        self.assertEqual(game.toDisplayString(), """--------------
 . X . . . . .
 o X . . . . .
 o X . . . . .
 X o . . . . .
 X o . . . . .
 X o . . . . .
--------------
-1-2-3-4-5-6-7
Current Player: o""")
        
        game = GameState();
        game.setup("121212")
        
        game.makeMove(3)
        self.assertEqual(game.isVictory(), False)
        game.makeMove(4)
        self.assertEqual(game.isVictory(), False)
        
        game.makeMove(1)
        self.assertEqual(game.isVictory(), True)
        
        self.assertEqual(game.toDisplayString(), """--------------
 . . . . . . .
 . . . . . . .
 X . . . . . .
 X o . . . . .
 X o . . . . .
 X o X o . . .
--------------
-1-2-3-4-5-6-7
Current Player: o""")
        game.unmakeMove(1)
        self.assertEqual(game.isVictory(), False)
        self.assertEqual(game.toDisplayString(), """--------------
 . . . . . . .
 . . . . . . .
 . . . . . . .
 X o . . . . .
 X o . . . . .
 X o X o . . .
--------------
-1-2-3-4-5-6-7
Current Player: X""")


if __name__ == "__main__":
    unittest.main()