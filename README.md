# Tetris Game with Heuristic Algorithm

# About The Game

#### This Tetris game is a modern rendition of the classic puzzle game, built using Python and the Pygame library. It features a custom heuristic-based algorithm for an automated gameplay mode, along with a fresh, pastel-themed UI.

----------------------------
# Features
----------------------------

#### Manual Play Mode: Traditional Tetris gameplay where the player controls the pieces.
#### Automatic Play Mode: Utilizes a heuristic algorithm for automated gameplay.
#### Customizable Settings: Allows for changes in board size and piece colors.
#### Pause and Resume Functionality: Players can pause and resume their game.

----------------------------
# Heuristic Algorithm
----------------------------

#### The game's heuristic algorithm evaluates moves based on factors such as lines cleared, holes created, stack bumpiness, and total stack height. Its goal is to maximize the score and lines cleared while minimizing the risk of game over.
----------------------------
# Requirements
----------------------------
To play the game, you'll need:

* Python 3.x
* Pygame
----------------------------
# Installation
----------------------------
#### Install Python: Ensure Python 3.x is installed on your system.
#### Install Pygame:
#### bash
#### Copy code
#### pip install pygame
----------------------------

#### Please make sure you import these packages as well
- import layout
- import random
- import time
- import copy

----------------------------
# Running the Game
----------------------------

#### Run the main Python script (e.g., main.py) from the terminal or an integrated development environment (IDE) to start the game.

----------------------------
# Controls
----------------------------

- Left/Right Arrow Keys: Move the tetromino left or right.
- Up Arrow Key: Rotate the tetromino.
- Down Arrow Key: Speed up the tetromino's descent.
- Spacebar: Instantly drop the tetromino.
- 'P' Key: Pause or resume the game.
- 'A' Key: Toggle automatic play mode.
- Contribution

----------------------------
#### Contributions to the game are welcome! Feel free to fork the repository, make your changes, and submit a pull request.
----------------------------
# Please note that this is the first version of the game and there are a few updates needs to be done for the algorithm to work better