# Minesweeper AI

This is an AI that plays the puzzle game minesweeper optimally.

Minesweeper is a logic-based game played on a grid of cells. The objective is to locate a number of randomly-placed "mines" by clicking on "safe" cells while avoiding the squares with mines. If the player clicks on a mine, the game ends. Otherwise, a number between 0 and 8 is displayed that identifies the total number of mines present in the eight neighboring squares. 

The AI works by representing the information about mines in a knowledge base that lends itself well to quick inferences. The following is an example of a sentence in the knowledge base:

{A, B, C, D, E, F, G, H} = 1

The above logical sentence says that out of cells A, B, C, D, E, F, G, H, exactly 1 of them is a mine.

There will be cases when there are no known safe moves (0 % chance of clicking on a mine). When this happens, the AI chooses a random cell. Hence, even though the AI plays optimally, it can lose. 

Video demonstration: https://youtu.be/fIpO5daehyM
