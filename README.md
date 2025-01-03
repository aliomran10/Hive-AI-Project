**Hive Game**

A Python implementation of the Hive board game, built using Pygame.

---

Table of Contents

1. Introduction

2. Features

3. Installation

4. How to Play

5. Converting to Executable

6. Contributing

---

**Introduction**

Hive is a highly strategic two-player board game where players compete to surround their opponent’s Queen Bee. This digital version recreates the board game experience using Python and Pygame, enabling players to enjoy Hive interactively on their computer while following the official rules.

---

**Features**

Interactive GUI for playing the Hive board game.

Adheres to official Hive rules: [Hive Rules](https://www.ultraboardgames.com/hive/game-rules.php)

Place pieces strategically to surround the opponent's Queen Bee.

Enforce rules like mandatory Queen placement by the fourth turn.

Prevent moves that split the hive into disconnected parts.

Unique movement for each piece based on its type.

A turn-based system for two players.

---

**Installation**

Follow these steps to set up the project on your local machine:

**Prerequisites**

Pygame library installed.

**Steps**

Clone this repository:

``` git clone https://github.com/aliomran10/Hive-AI-Project.git ```
``` cd Hive-AI-Project  ```

Install the required dependencies:

``` pip install pygame ```

Run the game:

``` python hive_game.py ```

---

**How to Play**

Players take turns placing or moving their pieces:

Introduce a new piece at any time, provided it touches at least one other piece.

Place your Queen Bee by the fourth turn.

After placing your Queen Bee, decide whether to move an existing piece or place a new one each turn.

Adhere to the unique movement rules for each piece (to be implemented as game prompts or documented later).

Surround your opponent's Queen Bee to win.

**Special Rules:**

Pieces cannot be moved if doing so splits the hive into disconnected parts.

All pieces must touch at least one other piece.

---

**Converting to Executable**

To share the game as a standalone executable, use PyInstaller:

Install PyInstaller:

``` pip install pyinstaller ```

Run the following command to generate the executable:

``` pyinstaller --onefile --icon=icon.ico hive_game.py ```

The executable file will be available in the dist folder.

---

**Contributing**

Contributions are welcome! If you'd like to improve the game, follow these steps:

1. Fork the repository.

2. Create a new branch:

``` git checkout -b feature-name ```

3. Commit your changes:

``` git commit -m "Add feature-name" ```

4. Push to your branch:

``` git push origin feature-name ```

5. Open a Pull Request.

---

Enjoy playing Hive and feel free to contribute to make it even better!
