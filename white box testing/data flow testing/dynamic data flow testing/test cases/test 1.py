import unittest
from wordle.wordle import Wordle

class TestWordle(unittest.TestCase):
    
    def test_word_initialization_and_guess(self):
        # Test specific word initialization
        game = Wordle(word="hello", display=False)
        self.assertEqual(game.word, "hello")
        
        # Test solving the game
        result = game.guess("hello")
        self.assertTrue(game.solved)
        self.assertEqual(result, [('h', 2), ('e', 2), ('l', 2), ('l', 2), ('o', 2)])
    
    def test_letter_position_mapping(self):
        game = Wordle(word="hello", display=False)
        self.assertEqual(game.letter_position['h'], {0})
        self.assertEqual(game.letter_position['l'], {2, 3})
    
    def test_max_attempts(self):
        game = Wordle(word="hello", max_attempts=3, display=False)
        game.guess("world")
        game.guess("there")
        game.guess("other")
        self.assertTrue(game.failed)
    
    def test_num_attempts_increment(self):
        game = Wordle(word="hello", display=False)
        self.assertEqual(game.num_attempts, 0)
        game.guess("world")
        self.assertEqual(game.num_attempts, 1)
        
    def test_game_solved(self):
        game = Wordle(word="hello", display=False)
        game.guess("hello")
        self.assertTrue(game.solved)
    
    def test_game_failed(self):
        game = Wordle(word="hello", max_attempts=2, display=False)
        game.guess("world")
        game.guess("there")
        self.assertTrue(game.failed)
    
    def test_attempts_repeat_detection(self):
        game = Wordle(word="hello", display=False)
        game.guess("world")
        game.guess("world")
        self.assertEqual(game.num_attempts, 1)  # Should not increment

