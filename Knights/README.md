# Logic Puzzle Solver

This is a program that uses propositional logic to solve logic puzzles. The rules of the puzzles are as follows:

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

*The objective of each puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.*

For example, consider a simple puzzle with just a single character named A. A says “I am both a knight and a knave.”

Logically, we might reason that if A were a knight, then that sentence would have to be true. But we know that the sentence cannot possibly be true, because A cannot be both a knight and a knave – we know that each character is either a knight or a knave, but not both. So, we could conclude, A must be a knave.

This was fairly simple but the puzzles get much trickier with multiple statements. The program solves the following puzzles using encoded knowledged bases:

<ins>Puzzle 0</ins>

A says “I am both a knight and a knave.”


<ins>Puzzle 1</ins>

A says “We are both knaves.”

B says nothing.

<ins>Puzzle 2</ins>

A says “We are the same kind.”

B says “We are of different kinds.”

<ins>Puzzle 3</ins>

A says either “I am a knight.” or “I am a knave.”, but you don’t know which.

B says “A said ‘I am a knave.’”

B then says “C is a knave.”

C says “A is a knight.”

<br>
Video demonstration: https://youtu.be/JykoocXiNtM
