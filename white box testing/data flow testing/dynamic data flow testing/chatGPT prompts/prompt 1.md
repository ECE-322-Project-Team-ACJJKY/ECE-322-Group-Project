# Prompt 1

> I would like to conduct dynamic data flow coverage white box software testing on a wordle application built in python. I need you to perform dynamic data flow ALL-USE testing on the code in this python file.
>
> What this means is that you should create a list of each and every variable that exists in the code, and for each one:
>
> 1. generate a concise table of tests to run the code through ALL-USE testing for the variable. Focus on the important tests, and include the inputs and expected results.
> 2. create unit tests in Python using unittest
>
> I will run the tests myself, so no need to run them for me

## Response

To conduct **dynamic data flow ALL-USE testing** for the provided Wordle application, we’ll identify variables in the code, create test cases for each variable to cover its all-use paths, and implement these as unit tests using Python's `unittest` framework.

---

### 1. Variables Identified and Use Analysis

Key variables from the code:

1. `self.word` – Stores the target word for the game.
2. `self.letter_position` – Maps letters to their positions in the target word.
3. `self.max_attempts` – Maximum attempts allowed.
4. `self.num_attempts` – Tracks the current number of attempts.
5. `self.alphabet` – Tracks correctness of each letter guessed.
6. `self.solved` – Indicates if the puzzle is solved.
7. `self.failed` – Indicates if the game is failed.
8. `self.attempts` – Stores all guesses and their results.

For each variable, we'll ensure all-definition-to-use (DU) pairs are tested.

---

### 2. Test Plan Table

Here’s a concise table outlining tests for the **ALL-USE** coverage of each variable.

| **Variable**      | **Test Case Input**          | **Expected Outcome**                                        |
|--------------------|------------------------------|------------------------------------------------------------|
| `self.word`        | Initialize with a specific word. Guess the same word. | `self.solved = True`, game solved.                         |
|                    | Initialize with a random word. Guess another word.    | Correct letter positions and counts are updated.           |
| `self.letter_position` | Initialize with "hello". Guess "hero".          | Matches letter positions correctly for 'h', 'e', and 'o'.  |
| `self.max_attempts`| Set max_attempts to 3. Guess 4 words.               | `self.failed = True` after 3rd guess.                      |
| `self.num_attempts`| Guess words until max_attempts.                    | Increments correctly per guess.                            |
| `self.alphabet`    | Guess "hero". Check dictionary values.             | Updates scores for each guessed letter.                    |
| `self.solved`      | Guess correct word.                                | `self.solved = True`.                                       |
| `self.failed`      | Exceed max attempts without solving.               | `self.failed = True`.                                       |
| `self.attempts`    | Guess "hello" twice.                               | Second guess flagged as a repeat.                          |

---

### 3. Unit Tests

Below are unit tests covering all-use paths for the variables.

```python
import unittest
from wordle import Wordle

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
    
    def test_alphabet_update(self):
        game = Wordle(word="hello", display=False)
        game.guess("hero")
        expected_alphabet = {
            'h': 2, 'e': 2, 'r': 0, 'o': 1, 
            **{chr(i): -1 for i in range(97, 123) if chr(i) not in 'hero'}
        }
        self.assertEqual(game.alphabet, expected_alphabet)
    
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
```

---

### Instructions

1. Save the unit tests in a separate file (e.g., `test_wordle.py`).
2. Use the following command to run the tests:

   ```bash
   python -m unittest test_wordle.py
   ```

Let me know if you'd like further clarification or help with additional testing approaches!

## Evalutation of Response

I had to remove the test: `test_alphabet_update`, as it makes no sense and expectedly failed, but the rest of the tests passed and achieved 75% of the Wordle class.
