# Twenty-nine (29) Card Game in Python

Welcome to the **Twenty-nine (29) Card Game** implemented in **Python**! This project recreates the classic multiplayer card game played mainly in South Asia, using Python for the game logic.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
**Twenty-nine (or 29)** is a trick-taking card game that involves four players divided into two teams. The game is played with a deck of 32 cards (8s, 9s, 10s, Jacks, Queens, Kings, Aces of each suit), and the objective is to reach 29 points through strategic card playing. This repository provides a Python-based implementation of the game, suitable for multiplayer or simulated gameplay.

## Features
- **Full Game Logic**: Implements rules of the Twenty-nine card game, including bidding, trump selection, and trick-taking.
- **Multiplayer Mode**: Allows four players, either human or AI-controlled.
- **Scoring System**: Includes point calculation and winning conditions.
- **Extensible Codebase**: Designed with modular classes to allow customization or further development.

## Getting Started
Follow these steps to clone the repository and start playing!

### Prerequisites
- **Python 3.6+** is required. Check your version by running:
```python
  python --version
```


## Installation
  Clone the repository
```bash
  git clone https://github.com/rubelliumm/29-Card-Game-Python.git
```

## How to play
    Navigate to the project directory:
```bash
  cd 29-Card-Game-Python
```
    Run the main python game script.
```python
  python3 main.py
```

  Game Rules:
      The game starts with a bidding phase, followed by a card-playing phase.
      Players attempt to win tricks by playing higher cards.
      The team that reaches 29 points first wins!

  Controls:
      Follow on-screen prompts to bid, select trumps, and play cards.

## Project Structure

Here's an overview of the key files and directories in this project:
    all files and directories is under src directory.
    [data_structure]: contains the CardList Data structure [card_list.py]

    Under game directory:
    twentynine.py: game's main entry point.
    bidding.py: bidding round of every single round.
    card.py: Contains classes for card objects and suits.
    board.py: board object functionality. that manage current points on board, highest card, winner of single turn etc.
    player.py: Contains the player class with methods for AI or human players.
    round.py: Logic for handling each round's phases, including trick-taking.
    state.py: game state management.
    utils.py: some utils functions.
    constants.py: some user specific constants.
    README.md: Documentation for this project.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request. For major changes, please open a discussion first.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
