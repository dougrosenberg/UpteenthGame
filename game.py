import time
import tkinter as tk
import tkinter.font as font
from collections import namedtuple
from tkinter import messagebox

import heuristic
from fifteen import Fifteen

TESTING = False

STAR_SYMBOL = '*'
STAR_BG_COLOR = 'yellow'
STANDARD_BG_COLOR = '#C0C0C0'
GAME_SIZE = 4
MAX_BOARD_SIZE = 10


# game = Fifteen(GAME_SIZE)

def Debug(mess, arg1=None, arg2=None):
    if arg2 is None:
        print(f"****** Debug: {mess}= {arg1}")
    else:
        print(f"****** Debug: {mess}= {arg1},{arg2}")


class Game:
    def __init__(self, gui, width):
        self.gf = tk.Frame(gui)
        self.width = self.height = width
        self.gui = gui
        self.gf = None
        self.buttons = []
        self.game = None
        self.text_info = TextInfo(app, width)
        self.num_moves = 0
        self.create_game_board()

    def computer_solve(self):
        self.num_moves = 0
        h = heuristic.Heuristic(tuple(self.game.tiles), self.width)
        solution = h.solve_using_heuristics()
        #        print(solution)
        if not solution:
            self.display_won_message()
        else:
            for d in solution:
                self.make_direction_move(d)

    def create_game_board(self):
        self.num_moves = 0
        if self.gf is not None:
            self.gf.grid_forget()
            self.gf.destroy()
            self.buttons = []
        self.gf = tk.Frame(self.gui)
        #        print('Create Game Board')
        board_size = self.text_info.board_str_size.get()
        if board_size.isdigit():
            board_size = int(board_size)
            if board_size > MAX_BOARD_SIZE:
                board_size = MAX_BOARD_SIZE
        else:
            board_size = 3
        self.height = self.width = board_size
        self.game = Fifteen(board_size)
        self.gf = tk.Frame(self.gui)
        size_board = max(100 * board_size, 300)
        self.gui.geometry(f'{size_board}x{size_board}')
        # self.tk =None
        # name the gui window
        # self.title("15 Game")
        # make a entry text xbo
        self.gf.grid_rowconfigure(10, weight=1)
        self.gf.grid_columnconfigure(0, weight=1)
        self.gf.f = font.Font(family='Helveca', size=12, weight='bold')

        star_button_id = self.height * self.width
        for index, button_id in enumerate(self.game.tiles):
            self.buttons.append(self.addButton(button_id, index))
        #        print(self.game)
        offset = 1
        for i in range(self.height):
            for j in range(self.width):
                self.buttons[i * self.width + j].grid(row=i + offset, column=j, columnspan=1)
        self.gf.pack()

    def make_move(self, button_id):
        button_id = int(button_id)
        #        print(f'You clicked on button {button_id}')
        temp = self.buttons[button_id]['text']
        if temp == '*':
            print('Invalid move on blank square')
            return
        star_id = int(self.game.get_star_location())
        # print('temp =', temp)
        # print('game.get_square(button_id) =', self.game.get_square(button_id))
        # assert int(temp) == game.get_square(button_id)
        if self.game.is_valid_move(button_id):
            self.game.make_move(button_id)
            new_star_button = self.buttons[button_id]
            old_star_button = self.buttons[star_id]
            old_star_button['text'] = new_star_button['text']
            new_star_button.configure(bg=STAR_BG_COLOR)
            old_star_button.configure(bg=STANDARD_BG_COLOR)
            new_star_button['text'] = STAR_SYMBOL
            new_star_button.update()
            old_star_button.update()
            # print(self.game)
            self.num_moves += 1
            if self.game.is_solved():
                self.display_won_message()

    def display_won_message(self):
        # Debug('Put up messsage box')
        messagebox.showinfo('You Won', f'Congratulations you won in {self.num_moves} moves !!!!!!!!!!!!.')

    def make_direction_move(self, direction):
        star_id = self.game.get_star_location()
        row_star, col_star = self.game.get_row_col(star_id)
        # print('Star Location = ', row_star, col_star)
        Point = namedtuple('Point', 'x,y')
        dir_dict = {'U': Point(0, -1), 'D': Point(0, +1), 'L': Point(-1, 0), 'R': Point(+1, 0)}
        new_row, new_col = (row_star + dir_dict[direction].y, col_star + dir_dict[direction].x)
        click_index = self.game.get_index(new_row, new_col)
        self.make_move(click_index)
        time.sleep(.02)

    def addButton(self, label_text_number, location_id):
        text_value = str(label_text_number)
        bg = STANDARD_BG_COLOR
        if label_text_number == 0:
            text_value = STAR_SYMBOL
            bg = STAR_BG_COLOR
        return tk.Button(self.gf, command=lambda: self.make_move(location_id), bg=bg, text=text_value,
                         height=4,
                         width=9)


class TextInfo(tk.Frame):
    def __init__(self, root, board_size):
        super().__init__(root, bg='pink', pady=3)
        # self.grid(row=1)
        self.pack()
        self.board_size = board_size
        # email
        self.board_str_size = tk.StringVar(self, board_size)
        board_size_label = tk.Label(self, text="Size (1 to 10) next reset")
        board_size_label.pack(fill='x', expand=True)

        size_entry = tk.Entry(self, textvariable=self.board_str_size, width=1)
        size_entry.pack(fill='x')
        size_entry.focus()


class Controls(tk.Frame):
    def __init__(self, root, game):
        super().__init__(root, bg='cyan', width=300, height=50, pady=3)
        # self.grid(row=1)
        self.pack()
        bluebutton = tk.Button(self, text="  Reset      ", fg="blue", command=game.create_game_board)
        redbutton = tk.Button(self, text="Computer Solve", command=game.computer_solve, fg="red")
        bluebutton.pack(side=tk.LEFT, padx=20)
        redbutton.pack(side=tk.RIGHT)


class App(tk.Tk):
    def __init__(self):
        # self.tk = None
        super().__init__()

        # configure the root window
        self.title('The Umteeth Game')
        self.geometry('400x400')
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)


# main program
# create the main window

app = App()
game = Game(app, GAME_SIZE)
controls = Controls(app, game)

# update the window
# center_window(gui)
app.mainloop()
