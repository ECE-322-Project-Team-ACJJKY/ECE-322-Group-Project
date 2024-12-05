# test/testcli.py

import unittest
from unittest.mock import patch
import sys
import io

from wordle import cli

class TestCli(unittest.TestCase):

    def test_main_no_arguments(self):
        # Simulate running 'cli.py' with no arguments
        inputs = ['apple', 'baker', 'cider', 'elder', 'fable', 'grape']
        with patch.object(sys, 'argv', ['cli.py']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Guess:", output)
            self.assertIn("Congratulations!", output)

    def test_main_random(self):
        # Simulate running 'cli.py' with '--random'
        inputs = ['apple', 'baker', 'cider', 'elder', 'fable', 'grape']
        with patch.object(sys, 'argv', ['cli.py', '--random']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Guess:", output)

    def test_main_seed(self):
        # Simulate running 'cli.py' with '--seed 42'
        inputs = ['apple', 'baker', 'cider', 'elder', 'fable', 'grape']
        with patch.object(sys, 'argv', ['cli.py', '--seed', '42']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Guess:", output)

    def test_main_solve(self):
        # Simulate running 'cli.py' with '--seed 42 --solve'
        with patch.object(sys, 'argv', ['cli.py', '--seed', '42', '--solve']), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Congratulations!", output)

    def test_main_helper(self):
        # Simulate running 'cli.py' with '--helper'
        inputs = ['arose', '00200', 'rimes', '00000', 'times', '22222']
        with patch.object(sys, 'argv', ['cli.py', '--helper']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Congratulations!", output)

    def test_main_random_game_failed(self):
        # Simulate failing the game in '--random' mode
        with patch.object(sys, 'argv', ['cli.py', '--random']), \
             patch('builtins.input', side_effect=['wrong'] * 6), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("The word was '", output)

    def test_main_helper_solution_found(self):
        # Simulate helper mode where the solution is found
        inputs = ['arose', '00200', 'rimes', '22222']
        with patch.object(sys, 'argv', ['cli.py', '--helper']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Congratulations!", output)
            self.assertIn("Solution: rimes", output)

    def test_main_helper_max_attempts_reached(self):
        # Simulate helper mode where maximum attempts are reached
        inputs = []
        for _ in range(6):
            inputs.extend(['arose', '00000'])  # Chosen word and result
        with patch.object(sys, 'argv', ['cli.py', '--helper']), \
             patch('builtins.input', side_effect=inputs), \
             patch('sys.exit') as mock_exit, \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:

            cli.main()
            output = mock_stdout.getvalue()
            self.assertIn("Attempt 6", output)
            self.assertNotIn("Congratulations!", output)

if __name__ == '__main__':
    unittest.main()
