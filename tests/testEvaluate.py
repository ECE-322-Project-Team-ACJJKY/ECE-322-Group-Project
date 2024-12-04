# test/testevaluate.py

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import io

from wordle.evaluate import run_solver_on_all_words, analyse_solver
from wordle.defaults import EVALUATION_FILE


class TestEvaluateSolver(unittest.TestCase):

    def setUp(self):
        # Mock the EVALUATION_FILE path
        self.evaluation_file_path = 'test_evaluation.json'
        self.evaluation_file = Path(self.evaluation_file_path)
        # Ensure the evaluation file does not exist before each test
        if self.evaluation_file.exists():
            self.evaluation_file.unlink()

    def tearDown(self):
        # Clean up the evaluation file after each test
        if self.evaluation_file.exists():
            self.evaluation_file.unlink()

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    @patch('wordle.evaluate.WordleSolver')
    @patch('wordle.evaluate.Wordle')
    @patch('wordle.evaluate.Vocabulary')
    def test_run_solver_on_all_words(self, MockVocabulary, MockWordle, MockWordleSolver, mock_evaluation_file):
        # Mock the Vocabulary to return a small sample vocab
        mock_vocab_instance = MockVocabulary.return_value
        mock_vocab_instance.vocab = ['apple', 'baker']

        # Mock the WordleSolver.solve method
        solver_instance = MockWordleSolver.return_value
        solver_instance.wordle.solved = True
        solver_instance.wordle.num_attempts = 4

        # Run the function
        result = run_solver_on_all_words()

        # Check that the result is as expected
        expected_result = {
            'status': {
                'apple': (True, 4),
                'baker': (True, 4)
            }
        }
        self.assertEqual(result, expected_result)

        # Check that the evaluation file was written
        self.assertTrue(self.evaluation_file.exists())
        with open(self.evaluation_file_path, 'r') as f:
            file_content = json.load(f)
            self.assertEqual(file_content, expected_result)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    @patch('wordle.evaluate.run_solver_on_all_words')
    def test_analyse_solver_with_existing_evaluation_file(self, mock_run_solver, mock_evaluation_file):
        # Mock the content of the evaluation file
        mock_data = {
            'status': {
                'apple': (True, 3),
                'baker': (False, 6)
            }
        }
        with open(self.evaluation_file_path, 'w') as f:
            json.dump(mock_data, f)

        # Run the function
        performance = analyse_solver()

        # Check that run_solver_on_all_words was not called
        mock_run_solver.assert_not_called()

        # Check the performance results
        expected_performance = {
            'total_count': 2,
            'success_count': 1,
            'failure_count': 1,
            'success_rate': 50.0,
            'average_attempts': 3.0
        }
        self.assertEqual(performance, expected_performance)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    @patch('wordle.evaluate.Vocabulary')
    @patch('wordle.evaluate.Wordle')
    @patch('wordle.evaluate.WordleSolver')
    def test_analyse_solver_without_existing_evaluation_file(self, MockWordleSolver, MockWordle, MockVocabulary, mock_evaluation_file):
        # Mock the Vocabulary to return a small sample vocab
        mock_vocab_instance = MockVocabulary.return_value
        mock_vocab_instance.vocab = ['apple', 'baker']

        # Mock the WordleSolver.solve method
        solver_instance = MockWordleSolver.return_value

        # Simulate different outcomes for each word
        def side_effect():
            solver_instance.wordle.solved = True
            solver_instance.wordle.num_attempts = 4

        solver_instance.solve.side_effect = side_effect

        # Run the function
        performance = analyse_solver()

        # Check that the evaluation file was created
        self.assertTrue(self.evaluation_file.exists())

        # Check the performance results
        expected_performance = {
            'total_count': 2,
            'success_count': 2,
            'failure_count': 0,
            'success_rate': 100.0,
            'average_attempts': 4.0
        }
        self.assertEqual(performance, expected_performance)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    def test_analyse_solver_with_no_success(self, mock_evaluation_file):
        # Mock the content of the evaluation file with no successes
        mock_data = {
            'status': {
                'apple': (False, 6),
                'baker': (False, 6)
            }
        }
        with open(self.evaluation_file_path, 'w') as f:
            json.dump(mock_data, f)

        # Run the function
        performance = analyse_solver()

        # Check the performance results
        expected_performance = {
            'total_count': 2,
            'success_count': 0,
            'failure_count': 2,
            'success_rate': 0.0,
            'average_attempts': float('nan')
        }
        self.assertEqual(performance['total_count'], expected_performance['total_count'])
        self.assertEqual(performance['success_count'], expected_performance['success_count'])
        self.assertEqual(performance['failure_count'], expected_performance['failure_count'])
        self.assertEqual(performance['success_rate'], expected_performance['success_rate'])
        # Since there are no successes, average_attempts should be NaN
        self.assertTrue(performance['average_attempts'] != performance['average_attempts'])  # NaN is not equal to itself

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    @patch('wordle.evaluate.analyse_solver')
    def test_main(self, mock_analyse_solver, mock_evaluation_file):
        # Mock the analyse_solver function
        mock_analyse_solver.return_value = {'success_rate': 100.0}
        # Capture the output
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            # Run the main block
            exec(open('wordle/evaluate.py').read())
            output = mock_stdout.getvalue()
            self.assertIn('"success_rate": 100.0', output)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    def test_run_solver_on_all_words_empty_vocab(self, mock_evaluation_file):
        # Mock the Vocabulary to return an empty vocab
        with patch('wordle.evaluate.Vocabulary') as MockVocabulary:
            mock_vocab_instance = MockVocabulary.return_value
            mock_vocab_instance.vocab = []

            # Run the function
            result = run_solver_on_all_words()

            # Check that the result is empty
            expected_result = {'status': {}}
            self.assertEqual(result, expected_result)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    def test_analyse_solver_no_evaluation_file(self, mock_evaluation_file):
        # Ensure the evaluation file does not exist
        if self.evaluation_file.exists():
            self.evaluation_file.unlink()

        # Mock run_solver_on_all_words to return a predefined result
        with patch('wordle.evaluate.run_solver_on_all_words') as mock_run_solver:
            mock_run_solver.return_value = {
                'status': {
                    'apple': (True, 4),
                    'baker': (True, 5)
                }
            }

            # Run the function
            performance = analyse_solver()

            # Check that run_solver_on_all_words was called
            mock_run_solver.assert_called_once()

            # Check the performance results
            expected_performance = {
                'total_count': 2,
                'success_count': 2,
                'failure_count': 0,
                'success_rate': 100.0,
                'average_attempts': 4.5
            }
            self.assertEqual(performance, expected_performance)

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    def test_analyse_solver_exception_handling(self, mock_evaluation_file):
        # Mock the evaluation file to contain invalid JSON
        with open(self.evaluation_file_path, 'w') as f:
            f.write('invalid json')

        # Run the function and check for exception handling
        with self.assertRaises(json.JSONDecodeError):
            analyse_solver()

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    def test_analyse_solver_zero_total_count(self, mock_evaluation_file):
        # Mock the content of the evaluation file with empty status
        mock_data = {'status': {}}
        with open(self.evaluation_file_path, 'w') as f:
            json.dump(mock_data, f)

        # Run the function
        performance = analyse_solver()

        # Check the performance results
        expected_performance = {
            'total_count': 0,
            'success_count': 0,
            'failure_count': 0,
            'success_rate': 0,
            'average_attempts': float('nan')
        }
        self.assertEqual(performance['total_count'], expected_performance['total_count'])
        self.assertEqual(performance['success_count'], expected_performance['success_count'])
        self.assertEqual(performance['failure_count'], expected_performance['failure_count'])
        self.assertEqual(performance['success_rate'], expected_performance['success_rate'])
        self.assertTrue(performance['average_attempts'] != performance['average_attempts'])  # NaN check

    @patch('wordle.evaluate.EVALUATION_FILE', new_callable=lambda: Path('test_evaluation.json'))
    @patch('wordle.evaluate.tqdm', side_effect=lambda x: x)
    def test_run_solver_on_all_words_progress_bar(self, mock_tqdm, mock_evaluation_file):
        # Mock the Vocabulary to return a sample vocab
        with patch('wordle.evaluate.Vocabulary') as MockVocabulary:
            mock_vocab_instance = MockVocabulary.return_value
            mock_vocab_instance.vocab = ['apple', 'baker', 'cider']

            # Mock the WordleSolver.solve method
            with patch('wordle.evaluate.WordleSolver') as MockWordleSolver:
                solver_instance = MockWordleSolver.return_value
                solver_instance.wordle.solved = True
                solver_instance.wordle.num_attempts = 4

                # Run the function
                result = run_solver_on_all_words()

                # Check that tqdm was called
                mock_tqdm.assert_called_once()

                # Check the result
                expected_result = {
                    'status': {
                        'apple': (True, 4),
                        'baker': (True, 4),
                        'cider': (True, 4)
                    }
                }
                self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
