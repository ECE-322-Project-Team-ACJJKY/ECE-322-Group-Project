# weak normal equivalence class testing
## what is weak normal equivalence class testing
designing a test case so that it covers one and only one invalid equivalence class and as many as possible valid equivalence classes
## test cases and outcomes
| id | description | expected outcome | actual outcome |
| ----------- | ----------- | ----------- | ----------- |
| valid |
| 1 | input a valid word, ie. a 5 letter word that is in the system's dictionary | the system accepts the word as a guess | as expected |
| invalid |
| 2 | input a word of invalid length (< 5 OR > 5) | error message | as expected |
| 3 | input a word with non-alphabetic characters | error message | as expected |
| 4 | input a word that is not in the system's dictionary | error message | as expected |
| outcomes |
| 5 | input a word that matches with the target word | all letters are green, success message | as expected |
| 6 | input a word that does not match the target word on the last guess | system exits with a lsot message | as expected |


## relevance of prompts and usefulness of replies and repeatability (ChatGPT)
Chat GPT was efficient in coming up with different test cases to generally test the wordle system, though it did give somewhat an excessive amount of tests than what was required for weak normal equivalence class testing. The results were relevant and mostly correct but sometimes would repeat itself in functionality. For example, when asked `could you come up with some weak normal equivalence black box test cases for a wordle cli system`, it gave some test cases what could be in the same partition of functionality. For example, it gave the inputs being `less than 5 characters` and `more than 5 characters` as two seperate test cases when they should be combined to one invalid test case. As well, it gives the behaviour test cases of `incorrect guess` and `exceeded allowed number of guesses` as two seperate test cases, when the latter test case wouldn't exist, as an incorrect guess would exit the system. Overall, the relevance and usefullness of ChatGPT's replies were pretty good, though needing a few minor modifications.