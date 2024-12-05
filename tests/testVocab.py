import unittest
import tempfile
import json
from pathlib import Path
from typing import Iterable

# Assuming the Vocabulary class is defined in the module vocabulary_module
from wordle.vocab import Vocabulary

class TestVocabulary(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        # Create paths for temporary files
        self.words_file = self.temp_dir_path / 'words.txt'
        self.vocab_cache = self.temp_dir_path / 'vocab_cache.json'
        self.index_cache = self.temp_dir_path / 'index_cache.json'

        # Define test constants
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.word_length = 5

        # Write test words to the temporary words file
        with open(self.words_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(['apple', 'berry', 'cherry', 'dates', 'elder']))

    def tearDown(self):
        # Clean up the temporary directory and files
        self.temp_dir.cleanup()

    def test_init_without_cache(self):
        """Test initialization when cache files do not exist."""
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        # Check if vocabulary and index are built
        self.assertTrue(hasattr(vocab, 'vocab'))
        self.assertTrue(hasattr(vocab, 'index'))
        self.assertIn('apple', vocab.vocab)
        self.assertEqual(vocab.word_length, self.word_length)
        # Check if cache files are created
        self.assertTrue(self.vocab_cache.is_file())
        self.assertTrue(self.index_cache.is_file())

    def test_init_with_cache(self):
        """Test initialization when cache files already exist."""
        # First, initialize to create cache files
        vocab1 = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        # Initialize again to use cache files
        vocab2 = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        # Verify that vocabularies are equal
        self.assertEqual(vocab1.vocab, vocab2.vocab)
        self.assertEqual(vocab1.index, vocab2.index)

    def test_build_vocabulary_use_cache_false(self):
        """Test build_vocabulary with use_cache set to False."""
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        # Modify the words file
        with open(self.words_file, 'a', encoding='utf-8') as f:
            f.write('\nfruit')
        # Rebuild vocabulary without using cache
        vocab.build_vocabulary(use_cache=False)
        self.assertIn('fruit', vocab.vocab)

    def test_build_index_use_cache_false(self):
        """Test build_index with use_cache set to False."""
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        # Modify the vocab
        vocab.vocab['fruit'] = self.word_length
        # Rebuild index without using cache
        vocab.build_index(use_cache=False)
        self.assertIn('f', vocab.index['letter'])
        self.assertIn('fruit', vocab.index['letter']['f'])

    def test_is_word(self):
        """Test the is_word method for existing and non-existing words."""
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=self.word_length,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertTrue(vocab.is_word('apple'))
        self.assertFalse(vocab.is_word('banana'))

    def test_missing_words_file(self):
        """Test initialization when the words file is missing."""
        # Remove the words file
        self.words_file.unlink()
        # Expect FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            Vocabulary(
                alphabet=self.alphabet,
                words_file=self.words_file,
                word_length=self.word_length,
                vocab_cache=self.vocab_cache,
                index_cache=self.index_cache
            )

    def test_corrupt_vocab_cache(self):
        """Test handling of a corrupt vocab cache file."""
        # Write invalid JSON to the vocab cache file
        with open(self.vocab_cache, 'w', encoding='utf-8') as f:
            f.write('invalid json')
        # Expect JSONDecodeError
        with self.assertRaises(json.JSONDecodeError):
            Vocabulary(
                alphabet=self.alphabet,
                words_file=self.words_file,
                word_length=self.word_length,
                vocab_cache=self.vocab_cache,
                index_cache=self.index_cache
            )

    def test_corrupt_index_cache(self):
        """Test handling of a corrupt index cache file."""
        # Write invalid JSON to the index cache file
        with open(self.index_cache, 'w', encoding='utf-8') as f:
            f.write('invalid json')
        # Expect JSONDecodeError
        with self.assertRaises(json.JSONDecodeError):
            Vocabulary(
                alphabet=self.alphabet,
                words_file=self.words_file,
                word_length=self.word_length,
                vocab_cache=self.vocab_cache,
                index_cache=self.index_cache
            )

    def test_words_of_different_lengths(self):
        """Test that words of incorrect length are excluded."""
        # Overwrite the words file with words of various lengths
        with open(self.words_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(['apple', 'banana', 'fig', 'go', 'honey']))
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=5,  # Set word length to 5
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertIn('apple', vocab.vocab)
        self.assertNotIn('banana', vocab.vocab)
        self.assertNotIn('fig', vocab.vocab)
        self.assertNotIn('go', vocab.vocab)
        self.assertNotIn('honey', vocab.vocab)  # 'honey' is 5 letters but was not in the list

    def test_frequency_attribute(self):
        """Test that the frequency attribute is correctly built."""
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=5,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertIn('letter', vocab.frequency)
        self.assertIn('letter_position', vocab.frequency)
        # Check frequency counts
        self.assertGreaterEqual(len(vocab.frequency['letter']), 1)
        self.assertGreaterEqual(len(vocab.frequency['letter_position']), 1)

    def test_custom_alphabet(self):
        """Test initialization with a custom alphabet."""
        custom_alphabet = 'abcde'
        vocab = Vocabulary(
            alphabet=custom_alphabet,
            words_file=self.words_file,
            word_length=5,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertEqual(vocab.alphabet, set(custom_alphabet))

    def test_invalid_word_length(self):
        """Test initialization with an invalid word length."""
        with self.assertRaises(ValueError):
            Vocabulary(
                alphabet=self.alphabet,
                words_file=self.words_file,
                word_length=0,  # Invalid word length
                vocab_cache=self.vocab_cache,
                index_cache=self.index_cache
            )

    def test_empty_words_file(self):
        """Test behavior when the words file is empty."""
        # Empty the words file
        with open(self.words_file, 'w', encoding='utf-8') as f:
            f.write('')
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=5,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertEqual(len(vocab.vocab), 0)

    def test_no_matching_words(self):
        """Test behavior when no words match the word length."""
        # Overwrite the words file with words of length not equal to 5
        with open(self.words_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(['six', 'seven', 'eight']))
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=5,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertEqual(len(vocab.vocab), 0)

    def test_nonexistent_cache_files(self):
        """Test initialization when cache files do not exist and use_cache is False."""
        # Ensure cache files do not exist
        if self.vocab_cache.exists():
            self.vocab_cache.unlink()
        if self.index_cache.exists():
            self.index_cache.unlink()
        vocab = Vocabulary(
            alphabet=self.alphabet,
            words_file=self.words_file,
            word_length=5,
            vocab_cache=self.vocab_cache,
            index_cache=self.index_cache
        )
        self.assertTrue(hasattr(vocab, 'vocab'))
        self.assertTrue(hasattr(vocab, 'index'))

if __name__ == '__main__':
    unittest.main()
