# Makrukthai-Analysis

Tkinter-based GUI application for visualizing a Makrukthai (Thai Chess) board. It allows users to input a FEN string, move pieces on the board, and add or remove pieces. The application also updates the FEN string based on the board's current state.

![Makrukthai Analysis Screenshot](https://raw.githubusercontent.com/natstpt/Makrukthai-Analysis/main/screenshot.png)

## Features

- 8x8 grid with Thai characters as column labels and numbers as row labels.
- Drag and drop pieces image from [PlayOK](https://www.playok.com/th/makruk/).
- FEN string updates when moving pieces on the board.
- Input FEN string in the Entry widget to update the board.
- Choose the side to move (white or black) using radio buttons.
- Add pieces to the board by clicking the "Add Piece" button.
- Analyze the board by sending the FEN string to [PyChess Analysis](https://www.pychess.org/analysis/makruk).
- Copy or paste the FEN string by clicking the button.
- Save the board image as a PNG file.

## Usage

To start the application, run the following command:

```bash
python makrukthaianalysis.py
