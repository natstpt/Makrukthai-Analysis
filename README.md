# Makrukthai-Analysis

![Makrukthai Analysis Screenshot](https://raw.githubusercontent.com/natstpt/Makrukthai-Analysis/main/screenshot.png)

Tkinter-based GUI application for visualizing a Makrukthai (Thai Chess) board. It allows users to input a FEN (Forsyth-Edwards Notation) string, move pieces on the board, and add or remove pieces. The application also updates the FEN string based on the board's current state.

1. The board is an 8x8 grid with Thai characters as column labels and numbers as row labels.
2. Pieces image from [https://www.playok.com/th/makruk/](https://www.playok.com/th/makruk/) can be dragged and dropped on the board. When a piece is moved, the FEN string is updated accordingly.
3. Users can input a FEN string in the Entry widget. Pressing a key updates the board to match the FEN string.
4. Users can choose the side to move (white or black) using radio buttons.
5. Users can add pieces to the board by clicking the "Add Piece" button, which opens a separate window with available pieces. Clicking a piece adds it to the board and updates the FEN string.
5. Users can analysis to sent FEN string to [www.pychess.org/analysis/makruk](https://www.pychess.org/analysis/makruk)
6. Users can copy or paste FEN string by clicking the button.
7. Users can save board image to png file.
