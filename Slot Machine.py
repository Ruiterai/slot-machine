import tkinter as tk
from tkinter import messagebox
import random

# Game Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

class SlotMachine:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")
        self.balance = 100  # Starting balance

        self.create_widgets()

    def create_widgets(self):
        # Balance Display
        self.balance_label = tk.Label(self.root, text=f"Balance: ${self.balance}", font=("Arial", 14))
        self.balance_label.pack()

        # Slot Display
        self.slot_frame = tk.Frame(self.root)
        self.slot_frame.pack()
        self.slots = [[tk.Label(self.slot_frame, text="?", font=("Arial", 24), width=5, height=2, relief="sunken") for _ in range(COLS)] for _ in range(ROWS)]

        for r in range(ROWS):
            for c in range(COLS):
                self.slots[r][c].grid(row=r, column=c, padx=10, pady=10)

        # Bet Input
        self.bet_label = tk.Label(self.root, text="Bet per line: ")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        # Lines Input
        self.lines_label = tk.Label(self.root, text="Number of lines: ")
        self.lines_label.pack()
        self.lines_entry = tk.Entry(self.root)
        self.lines_entry.pack()

        # Spin Button
        self.spin_button = tk.Button(self.root, text="Spin", command=self.spin, font=("Arial", 14), bg="green", fg="white")
        self.spin_button.pack(pady=10)

    def get_slot_machine_spin(self):
        all_symbols = []
        for symbol, count in symbol_count.items():
            all_symbols.extend([symbol] * count)

        columns = []
        for _ in range(COLS):
            column = random.sample(all_symbols, ROWS)
            columns.append(column)

        return columns

    def check_winnings(self, columns, lines, bet):
        winnings = 0
        winning_lines = []

        for line in range(lines):
            first_symbol = columns[0][line]
            if all(column[line] == first_symbol for column in columns):
                winnings += symbol_value[first_symbol] * bet
                winning_lines.append(line + 1)

        return winnings, winning_lines

    def spin(self):
        try:
            bet = int(self.bet_entry.get())
            lines = int(self.lines_entry.get())

            if not (MIN_BET <= bet <= MAX_BET):
                raise ValueError(f"Bet must be between ${MIN_BET} and ${MAX_BET}")
            if not (1 <= lines <= MAX_LINES):
                raise ValueError(f"Lines must be between 1 and {MAX_LINES}")

            total_bet = bet * lines
            if total_bet > self.balance:
                messagebox.showerror("Error", "Not enough balance!")
                return

            # Spin the slot machine
            slots = self.get_slot_machine_spin()
            for r in range(ROWS):
                for c in range(COLS):
                    self.slots[r][c].config(text=slots[c][r])

            # Calculate winnings
            winnings, winning_lines = self.check_winnings(slots, lines, bet)
            self.balance += winnings - total_bet
            self.balance_label.config(text=f"Balance: ${self.balance}")

            if winnings > 0:
                messagebox.showinfo("Result", f"You won ${winnings} on lines {winning_lines}!")
            else:
                messagebox.showinfo("Result", "No winnings this time!")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachine(root)
    root.mainloop()
