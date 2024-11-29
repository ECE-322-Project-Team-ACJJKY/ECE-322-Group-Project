# weak normal equivalence class testing
## wat is weak normal equivalence class testing
designing a test case so that it covers one and only one invalid equivalence class and as many as possible valid equivalence classes
## test cases and outcomes
| id | description | expected outcome | actual outcome |
| ----------- | ----------- | ----------- | ----------- |
| id | guessing the correct word | all the letters are green, a congratulations message is shown | as expected, exits the program |
| id | guessing an incorrect word with no correct letters but with all valid letter inputs and is a valid word | all guessed letters of the word are grey | as expected |
| id | guessing an incorrect word with a correct letter at the incorrect position | the correct letter is yellow | as expected |
| id | guessing an incorrect word with a correct letter at the correct position | the correct letter is green | as expected |
| id | guessing an incorrect word with a correct letter, where the letter appears twice in the word | if both at the correct potision, both letters are green; if one letter in the wrong position, one letter is green while the other is yellow; if both are in the wrong position, both are yellow | as expected |
| id | guessing a correct letter twice in a word that only uses that letter once | if in the correct position, one is green and one is grey; if in the incorrect position, one is yellow and one is grey | if in the correct position, one is green and the other is yellow; if in the incorrect position, both are yellow|
| id | guessing more words than permitted (6 times) with the incorrect word | the system will exit with a lost message | as expected |
| id | inputting non-alphabetic characters, including whitespace | some sort of error message | as expected, general error about not being a valid word |
| id | empty input | do nothing and does not take up a guess | as expected |
| id | wrong length of input (too long or too short) | some sort of error message about the length | as expected, general error about not being a valid word |
| id | guessing the same word multiple times | treats it the same as guessing a new word | error message about the word already being guessed |


## relvance of prompts and usefulness of replies and repeatability (ChatGPT)
Chat GPT was efficient in coming up with different test cases to generally test the wordle system, but was not efficient in discussing equivalence class testing and coming up with unique or many test cases for specifically testing with partioning. The results were relevant and mostly correct but surface level.