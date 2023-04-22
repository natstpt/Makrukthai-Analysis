# Makrukthai-Analysis

![Makrukthai Analysis Screenshot](https://raw.githubusercontent.com/natstpt/Makrukthai-Analysis/main/screencapture.png)

## Description

This project is a Tkinter-based GUI application for visualizing a Makrukthai (Thai Chess) board, designed to help users interact with and analyze their playing. Users can input a FEN string, move pieces on the board, add or remove pieces, and analyze the board using external resources. The application also updates the FEN string based on the board's current state. Key features include:

- **8x8 grid**: The board features Thai characters as column labels and numbers as row labels for easy navigation.
- **Drag and drop pieces**: High-quality piece images from [PlayOK](https://www.playok.com/th/makruk/) can be dragged and dropped onto the board.
- **FEN string updates**: The FEN string updates automatically when users move pieces on the board.
- **Input FEN string**: Users can input a FEN string in the Entry widget to update the board accordingly.
- **Choose the side to move**: Users can select the side to move (white or black) using radio buttons.
- **Start**: Users can change pieces on the board to start position by clicking the "Start" button.
- **Clear**: Users can remove all pieces on the board by clicking the "Clear" button.
- **Add Pieces**: Users can add pieces to the board by clicking the "Add Piece" button.
- **Analysis**: Users can analyze the board by sending the FEN string to [PyChess](https://www.pychess.org/analysis/makruk) for insights and recommendations.
- **Copy or Paste the FEN string**: Users can conveniently copy or paste the FEN string by clicking the appropriate button.
- **Save Image**: The board image can be saved as a PNG file for future reference or sharing.

These features work together to provide a user-friendly interface for visualizing, interacting with, and analyzing Makrukthai (Thai Chess).

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

Before you can use this project, ensure that you have the following software, libraries, and tools installed on your system:

1. [Python](https://www.python.org/) (version 3.9.13 or newer)
2. [pip](https://pip.pypa.io/en/stable/installation/) (Python package manager)

Additionally, this project depends on the following Python libraries:

- tkinter (version 8.6.12 or newer)
- pyautogui (version 0.9.48 or newer)
- pyperclip (version 1.8.2 or newer)
- pyinstaller (version 5.10.1 or newer)

These libraries will be installed automatically during the installation process described in the next section.

### Installation

To installing packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To start the application, run the following command:

```bash
python makrukthaianalysis.py
```

To create a standalone executable, run the following command:

```bash
pyinstaller --onefile --windowed makrukthaianalysis.py
```

## Contributing

Contributions are welcome! If you have any ideas or suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

I would like to express our gratitude to the following resources:

1. **Pieces image**: The piece images used in this project are sourced from [PlayOK](https://www.playok.com/th/makruk/).
2. **Analysis**: The board analysis feature in our project is made possible by leveraging the FEN string processing capabilities of [PyChess](https://www.pychess.org/analysis/makruk).
