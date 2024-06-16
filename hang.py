import tkinter as tk
from tkinter import messagebox
import random

# List of words for the hangman game
WORDS = ['python', 'hangman', 'challenge', 'programming', 'development']

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")
        
        # Randomly select a word from the WORDS list
        self.word = random.choice(WORDS)
        self.guessed = []
        self.mistakes = 0

        self.setup_gui()

    def setup_gui(self):
        # Frame for the canvas
        self.canvas_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.canvas_frame.grid(row=0, column=0, rowspan=5, padx=20, pady=20, sticky="nsew")
        
        # Canvas for drawing the hangman
        self.canvas = tk.Canvas(self.canvas_frame, width=300, height=300, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

        # Frame for the word display and input
        self.word_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.word_frame.grid(row=0, column=1, columnspan=2, pady=20, padx=20, sticky="nsew")

        # Label for displaying the word with blanks
        self.word_label = tk.Label(self.word_frame, text=' '.join(['_' for _ in self.word]), font=('Helvetica', 24), bg="#f0f0f0", fg="#333333")
        self.word_label.pack(pady=10)

        # Label for displaying messages
        self.message_label = tk.Label(self.root, text="Guess a letter:", font=('Helvetica', 18), bg="#f0f0f0", fg="#333333")
        self.message_label.grid(row=1, column=1, padx=10, sticky="e")

        # Entry widget for user input
        self.entry = tk.Entry(self.root, font=('Helvetica', 18), width=5)
        self.entry.grid(row=1, column=2, padx=10, sticky="w")
        self.entry.bind('<Return>', self.check_guess)

        # Button for submitting guesses
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_guess, font=('Helvetica', 18), bg="#4CAF50", fg="#ffffff")
        self.submit_button.grid(row=2, column=1, columnspan=2, pady=20)

        # Button for restarting the game
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=('Helvetica', 18), bg="#f44336", fg="#ffffff")
        self.restart_button.grid(row=3, column=1, columnspan=2, pady=20)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def check_guess(self, event=None):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showerror("Invalid input", "Please enter a single letter.")
            return

        if guess in self.guessed:
            messagebox.showwarning("Already guessed", "You have already guessed that letter.")
            return

        self.guessed.append(guess)
        if guess in self.word:
            self.update_word_label()
        else:
            self.mistakes += 1
            self.draw_hangman()

        if self.mistakes == 6:
            messagebox.showinfo("Game Over", f"You lost! The word was {self.word}")
            self.restart_game()
        elif '_' not in self.word_label.cget("text"):
            messagebox.showinfo("Congratulations", "You won!")
            self.restart_game()

    def update_word_label(self):
        display_word = ' '.join([letter if letter in self.guessed else '_' for letter in self.word])
        self.word_label.config(text=display_word)

    def draw_hangman(self):
        hangman_parts = [
            (self.canvas.create_line, (50, 250, 250, 250)),  # base
            (self.canvas.create_line, (100, 50, 100, 250)),  # pole
            (self.canvas.create_line, (100, 50, 200, 50)),   # beam
            (self.canvas.create_line, (200, 50, 200, 100)),   # rope
            (self.canvas.create_oval, (180, 100, 220, 140)),   # head
            (self.canvas.create_line, (200, 140, 200, 200)),  # body
            (self.canvas.create_line, (200, 160, 180, 180)), # left arm
            (self.canvas.create_line, (200, 160, 220, 180)), # right arm
            (self.canvas.create_line, (200, 200, 180, 240)), # left leg
            (self.canvas.create_line, (200, 200, 220, 240))  # right leg
        ]
        draw_func, args = hangman_parts[self.mistakes - 1]
        draw_func(*args)

    def restart_game(self):
        self.word = random.choice(WORDS)  # Randomly select a new word
        self.guessed = []
        self.mistakes = 0
        self.canvas.delete("all")
        self.word_label.config(text=' '.join(['_' for _ in self.word]))
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()