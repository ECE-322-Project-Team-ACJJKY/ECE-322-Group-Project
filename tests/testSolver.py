# test/testsolver.py

import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import io
from pathlib import Path
import json

from wordle.solver import WordleSolver
from wordle.wordle import Wordle
from wordle.vocab import Vocabulary
from wordle.defaults import COVERAGE_CACHE


class TestWordleSolver(unittest.TestCase):

    def setUp(self):
        # Set up a sample vocabulary and mock the Vocabulary class
        self.sample_vocab = ['apple', 'baker', 'cider', 'delta', 'eagle']
        self.vocab_mock = MagicMock()
        self.vocab_mock.vocab = self.sample_vocab
        self.vocab_mock.index = {
            'letter': {
                'a': {'apple', 'baker', 'delta', 'eagle'},
                'b': {'baker'},
                'c': {'cider'},
                'd': {'delta'},
                'e': {'apple', 'cider', 'delta', 'eagle'},
                'g': {'eagle'},
                'i': {'cider'},
                'k': {'baker'},
                'l': {'apple', 'delta', 'eagle'},
                'p': {'apple'},
                'r': {'baker', 'cider'},
                't': {'delta'},
            },
            'letter_position': {
                'a0': {'apple'},
                'b0': {'baker'},
                'c0': {'cider'},
                'd0': {'delta'},
                'e0': {'eagle'},
                'a1': {'baker'},
                'p1': {'apple'},
                # ... other positions
            }
        }
        self.vocab_mock.alphabet = set('abcdefghijklmnopqrstuvwxyz')

        # Mock the Vocabulary class to return our mock vocab
        self.patcher_vocab = patch('wordle.solver.Vocabulary', return_value=self.vocab_mock)
        self.mock_vocab_class = self.patcher_vocab.start()

        # Mock the coverage cache file path
        self.coverage_cache = 'test_coverage_cache.json'

        # Remove the coverage cache file if it exists
        if Path(self.coverage_cache).exists():
            Path(self.coverage_cache).unlink()

    def tearDown(self):
        # Stop the Vocabulary patcher
        self.patcher_vocab.stop()
        # Remove the coverage cache file if it was created
        if Path(self.coverage_cache).exists():
            Path(self.coverage_cache).unlink()

    def test_init_no_coverage_cache(self):
        """Test initialization when coverage cache does not exist."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        self.assertIsNotNone(solver.vocabulary)
        self.assertEqual(solver.valid_words, set(self.sample_vocab))
        self.assertEqual(solver.num_attempts, 0)
        self.assertEqual(solver.guesses, {})
        self.assertEqual(solver.known_letters, {})
        self.assertIsNotNone(solver.graph)
        self.assertIsNotNone(solver.coverage)
        # Check that coverage cache file is created
        self.assertTrue(Path(self.coverage_cache).exists())

    def test_init_with_coverage_cache(self):
        """Test initialization when coverage cache exists."""
        # Create a fake coverage cache file
        fake_coverage_data = {'apple': 50.0, 'baker': 40.0}
        with open(self.coverage_cache, 'w') as f:
            json.dump(fake_coverage_data, f)

        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        self.assertEqual(solver.coverage, fake_coverage_data)
        # Ensure that valid_words are set correctly
        self.assertEqual(solver.valid_words, set(self.sample_vocab))

    def test_build_graph(self):
        """Test the build_graph method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        solver.build_graph()
        # Check that the graph has nodes and edges
        self.assertTrue(len(solver.graph.nodes) > 0)
        self.assertTrue(len(solver.graph.edges) > 0)
        # Check that markers are set
        self.assertTrue(len(solver.markers) > 0)

    def test_calculate_coverage(self):
        """Test the calculate_coverage method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        # Test with letters 'a' and 'e'
        coverage = solver.calculate_coverage(['a', 'e'])
        self.assertIsInstance(coverage, float)
        self.assertGreaterEqual(coverage, 0)
        self.assertLessEqual(coverage, 100)

    def test_coverage_property(self):
        """Test the coverage cached_property."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        coverage = solver.coverage
        self.assertIsInstance(coverage, dict)
        self.assertEqual(set(coverage.keys()), set(self.sample_vocab))
        # Values should be floats between 0 and 100
        for value in coverage.values():
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 100)

    def test_reset_coverage(self):
        """Test the reset_coverage method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        coverage1 = solver.coverage
        solver.reset_coverage()
        self.assertFalse(hasattr(solver, 'coverage'))
        # Access coverage again; it should be recalculated
        coverage2 = solver.coverage
        self.assertIsNot(coverage1, coverage2)

    def test_eliminate(self):
        """Test the eliminate method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        initial_valid_words = solver.valid_words.copy()
        markers = {'a'}
        solver.eliminate(markers)
        # Words containing 'a' should be eliminated
        expected_valid_words = {word for word in self.sample_vocab if 'a' not in word}
        self.assertEqual(solver.valid_words, expected_valid_words)
        # Graph should have fewer nodes
        self.assertLess(len(solver.graph.nodes), len(initial_valid_words) + len(solver.markers))

    def test_top_coverage(self):
        """Test the top_coverage method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        top_options = solver.top_coverage(n=2)
        self.assertIsInstance(top_options, list)
        self.assertEqual(len(top_options), 2)
        for word, coverage in top_options:
            self.assertIn(word, self.sample_vocab)
            self.assertIsInstance(coverage, float)

    def test_best_options(self):
        """Test the best_options method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        options = solver.best_options()
        self.assertIsInstance(options, list)
        self.assertGreater(len(options), 0)
        for word, coverage in options:
            self.assertIn(word, self.sample_vocab)
            self.assertIsInstance(coverage, float)

    def test_get_options_from_valid_words(self):
        """Test the get_options_from_valid_words method."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        options = solver.get_options_from_valid_words()
        self.assertIsInstance(options, list)
        self.assertEqual(len(options), len(self.sample_vocab))
        for word, coverage in options:
            self.assertIn(word, self.sample_vocab)
            self.assertIsInstance(coverage, float)

    def test_handle_result(self):
        """Test the handle_result method with various scores."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        # Simulate guessing 'apple' and getting result '20212'
        result = [('a', 2), ('p', 0), ('p', 2), ('l', 1), ('e', 2)]
        solver.handle_result(result)
        # Check known_letters updates
        self.assertEqual(solver.known_letters['a'], 0)
        self.assertEqual(solver.known_letters['p'], 2)
        self.assertIsInstance(solver.known_letters['l'], set)
        self.assertIn(3, solver.known_letters['l'])
        self.assertEqual(solver.known_letters['e'], 4)
        # valid_words should be reduced
        self.assertLess(len(solver.valid_words), len(self.sample_vocab))

    def test_guess(self):
        """Test the guess method."""
        # Create a mock Wordle instance
        wordle_mock = MagicMock()
        wordle_mock.max_attempts = 6
        wordle_mock.num_attempts = 0
        wordle_mock.solved = False
        wordle_mock.failed = False
        # Simulate wordle.guess to return a result
        wordle_mock.guess.return_value = [('a', 0), ('p', 0), ('p', 0), ('l', 0), ('e', 0)]

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.guess()
        # Ensure that wordle.guess was called
        self.assertTrue(wordle_mock.guess.called)
        # num_attempts should have increased
        self.assertEqual(solver.num_attempts, 1)

    def test_solve(self):
        """Test the solve method."""
        # Create a mock Wordle instance
        wordle_mock = MagicMock()
        wordle_mock.max_attempts = 6
        wordle_mock.num_attempts = 0
        wordle_mock.solved = False
        wordle_mock.failed = False

        # Simulate wordle.guess responses
        def side_effect(guess):
            if guess == 'baker':
                return [('b', 0), ('a', 2), ('k', 0), ('e', 1), ('r', 0)]
            elif guess == 'apple':
                wordle_mock.solved = True
                return [('a', 2), ('p', 2), ('p', 2), ('l', 2), ('e', 2)]
            else:
                return [('a', 0), ('p', 0), ('p', 0), ('l', 0), ('e', 0)]

        wordle_mock.guess.side_effect = side_effect

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.solve()
        # Ensure that wordle.guess was called multiple times
        self.assertTrue(wordle_mock.guess.called)
        # num_attempts should be updated
        self.assertEqual(solver.num_attempts, 2)
        # wordle.solved should be True
        self.assertTrue(wordle_mock.solved)

    def test_calculate_coverage_with_omit_known_false(self):
        """Test calculate_coverage with omit_known=False."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        coverage = solver.calculate_coverage(['a', 'e'], omit_known=False)
        self.assertIsInstance(coverage, float)

    def test_best_options_few_valid_words(self):
        """Test best_options when valid_words are fewer than attempts left."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        solver.valid_words = {'apple'}
        # Simulate attempts left greater than valid_words
        if solver.wordle:
            solver.wordle.max_attempts = 6
            solver.wordle.num_attempts = 2
        options = solver.best_options()
        self.assertEqual(len(options), 1)
        self.assertEqual(options[0][0], 'apple')

    def test_guess_with_option(self):
        """Test the guess method with a provided option."""
        wordle_mock = MagicMock()
        wordle_mock.max_attempts = 6
        wordle_mock.num_attempts = 0
        wordle_mock.solved = False
        wordle_mock.failed = False
        wordle_mock.guess.return_value = [('a', 2), ('p', 2), ('p', 2), ('l', 2), ('e', 2)]

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.guess(option='apple')
        self.assertEqual(solver.num_attempts, 1)
        wordle_mock.guess.assert_called_with('apple')

    def test_guess_no_wordle(self):
        """Test the guess method when wordle is None."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        with self.assertLogs(level='ERROR') as cm:
            result = solver.guess()
        self.assertIn('No Wordle is defined.', cm.output[0])

    def test_solve_no_wordle(self):
        """Test the solve method when wordle is None."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        with self.assertLogs(level='ERROR') as cm:
            result = solver.solve()
        self.assertIn('No Wordle is defined.', cm.output[0])

    def test_eliminate_with_words(self):
        """Test the eliminate method with specific words to remove."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        remove_words = {'apple', 'baker'}
        solver.eliminate(markers=set(), words=remove_words)
        expected_valid_words = set(self.sample_vocab) - remove_words
        self.assertEqual(solver.valid_words, expected_valid_words)

    def test_handle_result_score_one(self):
        """Test handle_result with a score of 1 (letter correct but wrong position)."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        # Simulate result where 'a' is in the word but wrong position
        result = [('a', 1), ('p', 0), ('p', 0), ('l', 0), ('e', 0)]
        solver.handle_result(result)
        self.assertIsInstance(solver.known_letters['a'], set)
        self.assertIn(0, solver.known_letters['a'])
        # Valid words should be updated accordingly

    def test_handle_result_score_zero(self):
        """Test handle_result with a score of 0 (letter not in word)."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        result = [('z', 0), ('x', 0), ('q', 0), ('w', 0), ('e', 0)]
        solver.handle_result(result)
        # Letters 'z', 'x', 'q', 'w', 'e' should be eliminated
        self.assertNotIn('e', solver.valid_words)

    def test_eliminate_no_removal(self):
        """Test eliminate method when no words are eliminated."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        initial_valid_words = solver.valid_words.copy()
        markers = {'z'}  # Letter 'z' is not in any word
        solver.eliminate(markers)
        self.assertEqual(solver.valid_words, initial_valid_words)

    def test_calculate_coverage_empty_letters(self):
        """Test calculate_coverage with an empty list of letters."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        coverage = solver.calculate_coverage([])
        self.assertEqual(coverage, 0.0)

    def test_top_coverage_with_avoid_set(self):
        """Test top_coverage method with an avoid set."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        avoid_set = {'a', 'e'}
        top_options = solver.top_coverage(n=2, avoid_set=avoid_set)
        for word, _ in top_options:
            self.assertFalse(set(word).intersection(avoid_set))

    def test_reset_coverage_without_cached_property(self):
        """Test reset_coverage when coverage is not yet calculated."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        # Ensure coverage is not yet accessed
        self.assertFalse(hasattr(solver, 'coverage'))
        solver.reset_coverage()
        # No exception should be raised

    def test_guess_word_already_guessed(self):
        """Test that already guessed words are not suggested again."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        solver.guesses['apple'] = True
        options = solver.best_options()
        for word, _ in options:
            self.assertNotEqual(word, 'apple')

    def test_handle_result_no_result(self):
        """Test handle_result when result is None or empty."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        solver.handle_result(None)
        solver.handle_result([])
        # num_attempts should not increase
        self.assertEqual(solver.num_attempts, 0)

    def test_eliminate_with_no_markers_or_words(self):
        """Test eliminate when both markers and words are empty."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        initial_valid_words = solver.valid_words.copy()
        solver.eliminate(markers=set(), words=set())
        # valid_words should remain the same
        self.assertEqual(solver.valid_words, initial_valid_words)

    def test_best_options_with_known_letters(self):
        """Test best_options when known_letters are present."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        solver.known_letters = {'a': 0}
        options = solver.best_options()
        for word, _ in options:
            self.assertEqual(word[0], 'a')

    def test_calculate_coverage_full_coverage(self):
        """Test calculate_coverage when coverage is 100%."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        # Remove all words except one
        solver.valid_words = {'apple'}
        coverage = solver.calculate_coverage(['a', 'p', 'l', 'e'])
        self.assertEqual(coverage, 100.0)

    def test_handle_result_word_solved(self):
        """Test handle_result when the word is solved."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        result = [('a', 2), ('p', 2), ('p', 2), ('l', 2), ('e', 2)]
        solver.handle_result(result)
        self.assertEqual(solver.num_attempts, 1)
        # known_letters should have positions for all letters
        self.assertEqual(solver.known_letters['a'], 0)
        self.assertEqual(solver.known_letters['p'], 2)
        self.assertEqual(solver.known_letters['l'], 3)
        self.assertEqual(solver.known_letters['e'], 4)

    def test_top_coverage_no_options(self):
        """Test top_coverage when no options meet the criteria."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        top_options = solver.top_coverage(n=2, coverage_min=100)
        self.assertEqual(top_options, [])

    def test_guess_when_wordle_failed(self):
        """Test guess method when wordle has failed."""
        wordle_mock = MagicMock()
        wordle_mock.max_attempts = 6
        wordle_mock.num_attempts = 6
        wordle_mock.solved = False
        wordle_mock.failed = True

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.guess()
        # num_attempts should not increase
        self.assertEqual(solver.num_attempts, 0)

    def test_solve_when_wordle_already_solved(self):
        """Test solve method when wordle is already solved."""
        wordle_mock = MagicMock()
        wordle_mock.solved = True

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.solve()
        # num_attempts should remain zero
        self.assertEqual(solver.num_attempts, 0)
        # wordle.guess should not be called
        wordle_mock.guess.assert_not_called()

    def test_eliminate_with_nonexistent_marker(self):
        """Test eliminate with a marker that doesn't exist in the index."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        markers = {'z'}
        solver.eliminate(markers)
        # valid_words should remain the same
        self.assertEqual(solver.valid_words, set(self.sample_vocab))

    def test_eliminate_with_multiple_markers(self):
        """Test eliminate with multiple markers."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        markers = {'a', 'e'}
        solver.eliminate(markers)
        expected_valid_words = {word for word in self.sample_vocab if 'a' not in word and 'e' not in word}
        self.assertEqual(solver.valid_words, expected_valid_words)

    def test_guess_when_no_valid_words_left(self):
        """Test guess method when no valid words are left."""
        wordle_mock = MagicMock()
        wordle_mock.max_attempts = 6
        wordle_mock.num_attempts = 0
        wordle_mock.solved = False
        wordle_mock.failed = False

        solver = WordleSolver(wordle=wordle_mock, coverage_cache=self.coverage_cache)
        solver.valid_words = set()
        with self.assertRaises(IndexError):
            solver.guess()

    def test_handle_result_with_incorrect_scores(self):
        """Test handle_result with invalid score values."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        result = [('a', 3), ('p', -1), ('p', 2), ('l', 1), ('e', 2)]
        # Should handle invalid scores gracefully
        with self.assertRaises(ValueError):
            solver.handle_result(result)

    def test_calculate_coverage_with_nonexistent_letters(self):
        """Test calculate_coverage with letters not in the graph."""
        solver = WordleSolver(wordle=None, coverage_cache=self.coverage_cache)
        coverage = solver.calculate_coverage(['z', 'x', 'q'])
        self.assertEqual(coverage, 0.0)


if __name__ == '__main__':
    unittest.main()
