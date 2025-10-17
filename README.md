# Othello AI with Pygame UI

An interactive Reversi/Othello board game that pairs a minimax-based AI opponent with a modern Pygame interface. The project lets you play as black, choose an AI difficulty, and enjoy a polished experience inspired by [eothello.com](https://www.eothello.com/).

## Features

- Human-vs-AI Othello gameplay using the standard 8×8 board.
- Difficulty selector (Easy/Medium/Hard) that adjusts the minimax search depth.
- Click-to-play Pygame interface with:
  - Highlighted legal moves
  - Animated status updates
  - Score panel with live tallies
  - Last-move indicator
- End-of-game dialog with replay and difficulty change options.

## Getting Started

### Prerequisites

- Python 3.9+
- `pygame` 2.0 or newer

Install dependencies with:

```bash
python -m pip install pygame
```

### Run the game

From the repository root:

```bash
python src/othello.py
```

## Gameplay

1. Launch the game to see the difficulty picker.
2. Choose Easy (depth 1), Medium (depth 2), or Hard (depth 5).
3. You always play as black and move first. Click a highlighted square to place a disc.
4. The AI responds automatically. Continue until both sides are forced to pass.
5. Review the final score; replay, change difficulty, or exit.

## Project Structure

```
src/
├── othello.py      # Game logic and Pygame UI
├── linear.py       # Coursework remnants (unused by the game)
├── polynomial.py   # Coursework remnants (unused by the game)
└── testing.py      # Legacy tests/utilities
```

## Credits

- Original Othello logic by Panagiotis, Toby, and Aadya.
- UI refinements Panagiotis.
- Visual inspiration: [eothello.com](https://www.eothello.com/).

Enjoy the game, and feel free to submit issues or improvements!

