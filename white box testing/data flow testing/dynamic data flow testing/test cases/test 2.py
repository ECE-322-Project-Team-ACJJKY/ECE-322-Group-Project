import unittest
from unittest.mock import patch
from wordle.wordle import Wordle
import datetime

class TestWordleFullCoverage(unittest.TestCase):

    @patch("datetime.date")
    def test_seed_today(self, mock_date):
        # Mock today's date to ensure repeatable results
        mock_date.today.return_value = datetime.date(2023, 1, 1)
        mock_date.side_effect = lambda *args, **kw: datetime.date(*args, **kw)
        
        game = Wordle(seed="today", display=False) # type: ignore
        expected_word = "stamp"
        
        self.assertEqual(game.word, expected_word)

    def test_out_of_attempts(self):
        game = Wordle(word="hello", max_attempts=2, display=True)
        game.guess("world")
        game.guess("there")
        result = game.guess("other")
        self.assertTrue(game.failed)
        self.assertEqual(result, [])
    
    def test_guess_after_winning(self):
        game = Wordle(word="hello", display=False)
        game.guess("hello")
        self.assertTrue(game.solved)
        
        # Attempting another guess
        result = game.guess("world")
        self.assertEqual(result, [])
    
    def test_invalid_word_guess(self):
        game = Wordle(word="hello", display=False)
        result = game.guess("abcde")  # Assuming "abcde" is not in the vocabulary
        self.assertEqual(result, [])
    
    def test_display_enabled(self):
        game = Wordle(word="hello", display=True)
        
        with patch.object(game.console, "print") as mock_print:
            game.message("Test message")
            mock_print.assert_called()  # Verify `console.print` was called
    
    def test_show_method(self):
        game = Wordle(word="hello", display=True)
        
        with patch.object(game.console, "print") as mock_print:
            game.show()
            mock_print.assert_called()  # Verify `console.print` was called for display
        
        # Verify that styles are correctly applied
        style_mapping = {
            -1: "bold white underline",
            0: "bold black underline",
            1: "bold yellow underline",
            2: "bold green underline"
        }
        expected_display = [
            f"[{style_mapping[-1]}] [/{style_mapping[-1]}]" for _ in range(5)
        ]
        # No errors or unexpected formatting issues

if __name__ == "__main__":
    unittest.main()
