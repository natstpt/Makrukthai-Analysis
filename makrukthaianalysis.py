import tkinter as tk
from tkinter import filedialog
import pyperclip
import re
import pyautogui
import pygetwindow as gw
import os
import webbrowser

# Create the main window
root = tk.Tk()
root.title("Makrukthai Analysis by Natstpt")
root.geometry("642x714")

# Disable resizing
root.resizable(False, False)

# Create a chessboard with 8x8 squares
board_size = 8
square_size = 70
canvas = tk.Canvas(root, width=board_size * square_size,
                   height=board_size * square_size,
                   highlightthickness=1, highlightbackground='black')
canvas.pack()

# Place the chess pieces on the board
fen = "rnsmksnr/8/pppppppp/8/8/PPPPPPPP/8/RNSKMSNR w"
rows = fen.split('/')
pieces = {
    'r': 'br', 'n': 'bn', 's': 'bs', 'm': 'bm','x': 'bm2', 'k': 'bk', 'p': 'bp',
    'R': 'wr', 'N': 'wn', 'S': 'ws', 'M': 'wm','X': 'wm2', 'K': 'wk', 'P': 'wp'
}

# Create the chess pieces as images
piece_images = {}
for piece_code, piece_name in pieces.items():
    img = tk.PhotoImage(file=f"img/{piece_name}.png")
    img = img.subsample(1)
    piece_images[piece_code] = img

    # Add images for white pieces
    if piece_name[0] == 'w':
        piece_images[piece_code.upper()] = img

# Create a dictionary to keep track of the piece positions
piece_positions = {}

# Draw the board and place the pieces
def draw_board(fen):
    # Pad the FEN string with '/' characters to ensure it has 8 rows
    rows = fen.split('/')
    while len(rows) < 8:
        rows.append('8')
    while len(rows) > 8:
        rows.pop()

    # Truncate each row to 8 characters to ensure it has 8 squares
    rows = [re.sub(r'\d', lambda m: ' ' * int(m.group(0)), row)[:8] for row in rows]

    for row_idx, row in enumerate(rows):
        for col_idx in range(8):
            color = "#F4B464"
            canvas.create_rectangle(
                col_idx * square_size, row_idx * square_size, (col_idx + 1) * square_size, (row_idx + 1) * square_size, fill=color
            )

        for col_idx, char in enumerate(row):
            piece = pieces.get(char)
            if piece:
                img = piece_images[char]
                piece_id = canvas.create_image(col_idx * square_size + square_size/2, row_idx * square_size + square_size/2,
                                               anchor='center', image=img, tags=char)
                piece_positions[piece_id] = (col_idx, row_idx)

                # Bind the piece to drag-and-drop events
                canvas.tag_bind(piece_id, '<Button-1>', on_piece_clicked)
                canvas.tag_bind(piece_id, '<B1-Motion>', on_piece_dragged)
                canvas.tag_bind(piece_id, '<ButtonRelease-1>',
                                on_piece_dropped)

    """ # Draw the column eng labels
    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] """

    # Draw the column thai labels
    labels = ['ก', 'ข', 'ค', 'ง', 'จ', 'ฉ', 'ช', 'ญ']

    for col_idx in range(8):
        label = labels[col_idx]
        canvas.create_text(col_idx * square_size + square_size/2 + 30,
                       8 * square_size - square_size/2 + 26, text=label)

    # Draw the row labels
    for row_idx in reversed(range(8)):
        label = str(8 - row_idx)
        canvas.create_text(555, row_idx * square_size + 15, text=label)

    # Update the fen_entry with the current FEN
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, fen)

def on_piece_clicked(event):
    # Get the ID of the clicked piece
    piece_id = canvas.find_withtag(tk.CURRENT)[0]

    # Raise the clicked piece to the top of the canvas
    canvas.tag_raise(piece_id)

    # Set the piece as the current drag piece
    canvas.drag_piece = piece_id

    # Get the initial position of the piece
    x, y = event.x, event.y
    piece_x, piece_y = canvas.coords(piece_id)
    canvas.drag_piece_offset = (piece_x - x, piece_y - y)

def on_piece_dragged(event):
    # If there is no current drag piece, do nothing
    if not hasattr(canvas, 'drag_piece'):
        return

    # Move the drag piece to the current mouse position
    x, y = event.x, event.y
    dx, dy = canvas.drag_piece_offset
    canvas.coords(canvas.drag_piece, x + dx, y + dy)

    # Check if the piece is being dragged off the canvas
    bbox = canvas.bbox(canvas.drag_piece)
    if bbox[0] < 0:
        canvas.move(canvas.drag_piece, -bbox[0], 0)
    elif bbox[2] > board_size * square_size:
        canvas.move(canvas.drag_piece, board_size * square_size - bbox[2], 0)
    if bbox[1] < 0:
        canvas.move(canvas.drag_piece, 0, -bbox[1])
    elif bbox[3] > board_size * square_size:
        canvas.move(canvas.drag_piece, 0, board_size * square_size - bbox[3])

def fen_from_piece_positions():
    board = [['' for _ in range(board_size)] for _ in range(board_size)]
    for piece_id, (col_idx, row_idx) in piece_positions.items():
        piece_char = None
        for tag in canvas.gettags(piece_id):
            if tag in pieces:
                piece_char = tag
                break
        if piece_char is not None:
            board[row_idx][col_idx] = piece_char

    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for piece in row:
            if piece == '':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    # Get the side to move from the current FEN string
    side_to_move = fen.split()[-1]

    # Add the side to move to the new FEN string
    return '/'.join(fen_rows) + ' ' + side_to_move

def on_piece_dropped(event):
    # If there is no current drag piece, do nothing
    if not hasattr(canvas, 'drag_piece'):
        return

    # Get the ID of the dropped piece
    piece_id = canvas.drag_piece

    # Determine the new position of the piece
    x, y = event.x, event.y
    col_idx = int(x / square_size)
    row_idx = int(y / square_size)

    # Check if the piece is dropped outside the 8x8 board
    if 0 <= col_idx < board_size and 0 <= row_idx < board_size:
        # Move the piece to the new position
        canvas.coords(piece_id, col_idx * square_size + square_size /
                      2, row_idx * square_size + square_size / 2)

        # Update the piece position in the piece_positions dictionary
        old_col_idx, old_row_idx = piece_positions[piece_id]
        piece_positions[piece_id] = (col_idx, row_idx)
    else:
        # Remove the piece from the piece_positions dictionary
        del piece_positions[piece_id]

        # Delete the piece from the canvas
        canvas.delete(piece_id)

    # Reset the drag piece variables
    del canvas.drag_piece
    del canvas.drag_piece_offset

    # Update the FEN string
    new_fen = fen_from_piece_positions()

    # Update the fen_entry with the new FEN
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, new_fen)

    # Update the FEN string after moving the piece
    global fen
    fen = fen_from_piece_positions()

def update_board():
    new_fen = fen_entry.get()
    canvas.delete("all")
    draw_board(new_fen)

    # Update the piece_positions dictionary with the new piece positions
    for piece_id, (col_idx, row_idx) in piece_positions.items():
        piece_positions[piece_id] = (col_idx, row_idx)

        # Move the piece to its new position
        x = col_idx * square_size + square_size/2
        y = row_idx * square_size + square_size/2
        canvas.coords(piece_id, x, y)

    # Update the fen_entry with the new FEN
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, new_fen)


def on_fen_changed(event):
    new_fen = fen_entry.get()
    canvas.delete("all")
    draw_board(new_fen)

    # Update the piece_positions dictionary with the new piece positions
    for piece_id, (col_idx, row_idx) in piece_positions.items():
        piece_positions[piece_id] = (col_idx, row_idx)

        # Move the piece to its new position
        x = col_idx * square_size + square_size/2
        y = row_idx * square_size + square_size/2
        canvas.coords(piece_id, x, y)

def start_game():
    global fen
    fen = "rnsmksnr/8/pppppppp/8/8/PPPPPPPP/8/RNSKMSNR w"
    canvas.delete("all")
    piece_positions.clear()
    draw_board(fen)

    # Update the fen_entry with the new FEN
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, fen)

    # Set the selected radio button to "White"
    side_var.set("w")


def clear_board():
    global fen
    fen = "4k3/8/8/8/8/8/8/3K4 w"
    canvas.delete("all")
    piece_positions.clear()
    draw_board(fen)

    # Update the fen_entry with the new FEN
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, fen)

    # Set the selected radio button to "White"
    side_var.set("w")

def update_fen_side():
    global fen
    current_fen = fen_entry.get()
    side = side_var.get()
    fen_parts = current_fen.split()
    fen_parts[-1] = side
    fen = ' '.join(fen_parts)
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, fen)
    canvas.delete("all")
    draw_board(fen)

def fen_entry_changed(event):
    fen_text = fen_entry.get()
    last_char = fen_text[-1] if fen_text else ''

    if last_char == 'w':
        side_var.set('w')
    elif last_char == 'b':
        side_var.set('b')
    else:
        side_var.set(None)

def on_entry_click(event):
    entry_widget = event.widget
    x = event.x
    clicked_position = entry_widget.index(tk.INSERT)
    entry_widget.icursor(clicked_position)  

def on_key_release(event):    
    cursor_position = fen_entry.index(tk.INSERT)
    on_fen_changed(event)
    fen_entry_changed(event)
    fen_entry.icursor(cursor_position)


# Add this function to create a separate window displaying all the available pieces
def display_pieces():
    piece_window = tk.Toplevel(root)
    piece_window.title("Add Pieces")
    piece_window.geometry("350x300")

    # Disable resizing
    piece_window.resizable(False, False)

    piece_frame = tk.Frame(piece_window, padx=10, pady=10)
    piece_frame.pack(side="top", fill="x")    

    displayed_piece_images = {k: v for k, v in piece_images.items() if k not in ('k', 'K')}  # Exclude 'k' and 'K' pieces

    for i, (piece_code, img) in enumerate(displayed_piece_images.items()):
        piece_button = tk.Button(piece_frame, image=img, command=lambda p_code=piece_code: on_piece_selected(p_code))
        piece_button.image = img
        piece_button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

def on_piece_selected(piece_code):
    add_piece_to_fen(piece_code)

def add_piece_to_fen(piece_code):
    global fen
    fen_parts = fen.split()
    fen_rows = fen_parts[0].split('/')
    row_updated = False

    for i, row in enumerate(fen_rows):
        if row_updated:
            break

        new_row = []
        empty_count = 0
        for part in row:
            if part.isdigit():
                empty_count = int(part)
                if empty_count > 0 and not row_updated:
                    if empty_count > 1:
                        new_row.append(str(empty_count - 1))
                    new_row.append(piece_code)
                    row_updated = True
                else:
                    new_row.append(str(empty_count))
            else:
                new_row.append(part)

        fen_rows[i] = ''.join(new_row)

    new_fen = '/'.join(fen_rows) + ' ' + fen_parts[1]
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, new_fen)
    canvas.delete("all")
    draw_board(new_fen)

     # Update the FEN string after moving the piece
    fen = new_fen

# Copy FEN string to clipboard
def copy_fen_to_clipboard():
    modified_fen = fen.replace('x', 'm~').replace('X', 'M~')
    pyperclip.copy(modified_fen)

def paste_to_entry():
    global fen
    clipboard_fen = pyperclip.paste()
    fen_entry.delete(0, tk.END)
    fen_entry.insert(0, clipboard_fen)
    fen_entry_changed(clipboard_fen)    
    draw_board(clipboard_fen)

    # Update the FEN string after moving the piece
    fen = clipboard_fen

def save_board_image():
    active_window = gw.getActiveWindow()
    x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Define the crop margins run py file
    left_margin = 49
    right_margin = 50
    top_margin = 38
    bottom_margin = 162

    """ # Define the crop margins build exe file
    left_margin = 43
    right_margin = 43
    top_margin = 32
    bottom_margin = 155 """

    # Crop the image
    cropped_screenshot = screenshot.crop((left_margin, top_margin, width - right_margin, height - bottom_margin))

    # Open a file dialog to let the user choose the file storage location and specify a filename
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    # If the user chose a file path, save the cropped image to that path
    if file_path:
        cropped_screenshot.save(file_path)
        os.startfile(file_path)  # Open the saved PNG file with the default image viewer

def fen_analysis_url():
    pychess_url = "https://www.pychess.org/analysis/makruk?fen="
    modified_fen = fen.replace('x', 'm~').replace('X', 'M~')
    analysis_url = pychess_url + modified_fen
    webbrowser.open(analysis_url)

# Create a frame for the FEN label and entry widgets
fen_frame = tk.Frame(root, padx=10, pady=10)
fen_frame.pack(side="top", fill="x")

# Create a label and entry widget for FEN input
fen_label = tk.Label(fen_frame, text="FEN ")
fen_label.pack(side="left")

fen_entry = tk.Entry(fen_frame, width=80)
fen_entry.pack(side="left", padx=(5, 0))
fen_entry.bind('<KeyRelease>', on_key_release)

# Create a frame for the buttons
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(side="top")

# Create a frame for the radio buttons
radio_frame = tk.Frame(root, padx=10, pady=10)
radio_frame.pack(side="top", fill="x")

# Create a button to Start Position
start_button = tk.Button(button_frame, text="Start", command=start_game)
start_button.pack(side="left", padx=(50, 5))

# Create a button to Clear the board
clear_board_button = tk.Button(
    button_frame, text="Clear", command=clear_board)
clear_board_button.pack(side="left", padx=5)

# Create a frame for the radio buttons
radio_frame = tk.Frame(root, padx=10, pady=10)
radio_frame.pack(side="top", fill="x")

# Create radio buttons to choose white or black side
side_var = tk.StringVar()
side_var.set("w")
white_radio = tk.Radiobutton(
    radio_frame, text="White", variable=side_var, value="w", command=update_fen_side)
white_radio.pack(side="left")
black_radio = tk.Radiobutton(
    radio_frame, text="Black", variable=side_var, value="b", command=update_fen_side)
black_radio.pack(side="left")

# Add this line inside the button_frame
add_piece_button = tk.Button(button_frame, text="Add Pieces", command=display_pieces)
add_piece_button.pack(side="left", padx=5)

# Add this line inside the button_frame
analysis_button = tk.Button(button_frame, text="Analysis", command=fen_analysis_url)
analysis_button.pack(side="left", padx=5)

# Add this line inside the button_frame
copy_button = tk.Button(button_frame, text="Copy FEN", command=copy_fen_to_clipboard)
copy_button.pack(side="left", padx=5)

# Add this line inside the button_frame
paste_button = tk.Button(button_frame, text="Paste FEN", command=paste_to_entry)
paste_button.pack(side="left", padx=5)

# Add this line inside the button_frame
save_button = tk.Button(button_frame, text="Save Image", command=save_board_image)
save_button.pack(side="left", padx=5)

# Draw the initial board
draw_board(fen)

# Run the main loop
root.mainloop()
