import unittest
from unittest.mock import patch
import datetime

# Assuming the Wordle class is defined in the module named wordle_module
from wordle.wordle import Wordle

class TestWordle(unittest.TestCase):

    def test_word_in_vocab(self):
        """Test initialization with a word in the vocabulary."""
        game = Wordle(word='apple')
        self.assertEqual(game.word, 'apple')
        self.assertFalse(game.solved)
        self.assertFalse(game.failed)

    def test_word_not_in_vocab(self):
        """Test initialization with a word not in the vocabulary."""
        game = Wordle(word='zzzzz')
        self.assertNotEqual(game.word, 'zzzzz')  # Should pick a random word instead

    @patch('datetime.date')
    def test_word_none_seed_today(self, mock_date):
        """Test initialization with seed 'today'."""
        mock_date.today.return_value = datetime.date(2021, 1, 1)
        game1 = Wordle(word=None, seed='today')
        game2 = Wordle(word=None, seed='today')
        self.assertEqual(game1.word, game2.word)

    def test_word_none_seed_number(self):
        """Test initialization with a numeric seed."""
        seed = 12345
        game1 = Wordle(word=None, seed=seed)
        game2 = Wordle(word=None, seed=seed)
        self.assertEqual(game1.word, game2.word)

    def test_guess_correct(self):
        """Test guessing the correct word."""
        game = Wordle(word='apple')
        result = game.guess('apple')
        self.assertTrue(game.solved)
        self.assertFalse(game.failed)
        expected_result = [('a',2), ('p',2), ('p',2), ('l',2), ('e',2)]
        self.assertEqual(result, expected_result)

    def test_guess_incorrect(self):
        """Test guessing an incorrect word."""
        game = Wordle(word='apple')
        result = game.guess('berry')
        self.assertFalse(game.solved)
        self.assertFalse(game.failed)
        expected_result = [('b',0), ('e',1), ('r',0), ('r',0), ('y',0)]
        self.assertEqual(result, expected_result)

    def test_no_more_attempts(self):
        """Test guessing after maximum attempts have been reached."""
        game = Wordle(word='apple', max_attempts=1)
        game.guess('berry')
        game.guess('cherry')  # Should display "No more attempts left."
        self.assertEqual(game.num_attempts, game.max_attempts)
        self.assertTrue(game.failed)

    def test_already_solved(self):
        """Test guessing after the word has been solved."""
        game = Wordle(word='apple')
        game.guess('apple')
        self.assertTrue(game.solved)
        game.guess('berry')  # Should display "Wordle is already solved!"
        self.assertEqual(game.num_attempts, 1)

    def test_invalid_word(self):
        """Test guessing an invalid word not in the vocabulary."""
        game = Wordle(word='apple')
        result = game.guess('zzzzz')
        self.assertEqual(game.num_attempts, 0)
        self.assertFalse(game.solved)

    def test_already_attempted(self):
        """Test guessing a word that has already been attempted."""
        game = Wordle(word='apple')
        game.guess('berry')
        num_attempts_before = game.num_attempts
        game.guess('berry')  # Should display "Already attempted 'berry'."
        self.assertEqual(game.num_attempts, num_attempts_before)

    def test_failed_to_solve(self):
        """Test game state when failing to solve within maximum attempts."""
        game = Wordle(word='apple', max_attempts=1)
        game.guess('berry')
        self.assertFalse(game.solved)
        self.assertTrue(game.failed)
        game.guess('cherry')
        self.assertEqual(game.num_attempts, 1)

    def test_guess_with_various_scores(self):
        """Test scoring logic with various letter positions."""
        game = Wordle(word='apple')
        result = game.guess('alley')
        expected_result = [('a',2), ('l',1), ('l',1), ('e',1), ('y',0)]
        self.assertEqual(result, expected_result)

    def test_show_with_default_style(self):
        """Test display of the game board with default styling."""
        game = Wordle(word='apple', display=True)
        game.guess('berry')
        game.show()

    def test_show_with_custom_style(self):
        """Test display of the game board with custom styling."""
        game = Wordle(word='apple', display=True)
        game.guess('berry')
        custom_style = {
            -1: "white",
            0: "black",
            1: "yellow",
            2: "green"
        }
        game.show(style=custom_style)

    def test_message_with_display_true(self):
        """Test the message function with display enabled."""
        game = Wordle(display=True)
        game.message("Test message", style="bold red")

    def test_message_with_display_false(self):
        """Test the message function with display disabled."""
        game = Wordle(display=False)
        game.message("Test message", style="bold red")

if __name__ == '__main__':
    unittest.main()
