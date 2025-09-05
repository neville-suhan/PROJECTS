import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic
import os

USERS_FILE = "users.txt"

# Ensure users.txt exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        pass

class GuessingGameApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎯 Number Guessing Game")
        self.window.geometry("500x400")
        self.window.config(bg="#f0f8ff")
        self.username = None
        self.game = GameLogic()

        self.show_login_screen()
        self.window.mainloop()

    # ---------------- LOGIN SCREEN ----------------
    def show_login_screen(self):
        self.clear_window()

        tk.Label(self.window, text="Login / Signup", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=20)

        tk.Label(self.window, text="Username:", font=("Arial", 14), bg="#f0f8ff").pack()
        username_entry = tk.Entry(self.window, font=("Arial", 14))
        username_entry.pack()

        tk.Label(self.window, text="Password:", font=("Arial", 14), bg="#f0f8ff").pack()
        password_entry = tk.Entry(self.window, show="*", font=("Arial", 14))
        password_entry.pack()

        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if self.authenticate_user(username, password):
                self.username = username
                self.show_game_screen()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        def signup():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if username and password:
                if self.register_user(username, password):
                    messagebox.showinfo("Success", "Account created! Please log in.")
                else:
                    messagebox.showerror("Error", "Username already exists!")
            else:
                messagebox.showerror("Error", "Please fill in all fields!")

        tk.Button(self.window, text="Login", font=("Arial", 14, "bold"), bg="#90ee90", command=login).pack(pady=10)
        tk.Button(self.window, text="Signup", font=("Arial", 14, "bold"), bg="#add8e6", command=signup).pack()

    # ---------------- GAME SCREEN ----------------
    def show_game_screen(self):
        self.clear_window()
        self.game.reset_game()

        tk.Label(self.window, text=f"Welcome {self.username}!", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.window, text="Guess the number between 1 and 100", font=("Arial", 14), bg="#f0f8ff").pack()

        guess_entry = tk.Entry(self.window, font=("Arial", 14))
        guess_entry.pack(pady=10)

        result_label = tk.Label(self.window, text="", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="purple")
        result_label.pack()

        hint_label = tk.Label(self.window, text="", font=("Arial", 12), bg="#f0f8ff", fg="blue")
        hint_label.pack(pady=5)

        def submit_guess():
            try:
                guess = int(guess_entry.get())
                result = self.game.check_guess(guess)
                result_label.config(text=result)
                if result == "Correct!":
                    messagebox.showinfo("Winner!", f"🎉 You guessed it in {self.game.attempts} tries!")
                    self.show_game_screen()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        def get_hint():
            hint_label.config(text=self.game.get_hint())

        def quit_game():
            answer = self.game.reveal_answer()
            messagebox.showinfo("Game Over", f"The correct number was {answer}")
            self.show_game_screen()

        tk.Button(self.window, text="Submit Guess", font=("Arial", 14, "bold"), bg="#90ee90", command=submit_guess).pack(pady=5)
        tk.Button(self.window, text="Get Hint", font=("Arial", 14, "bold"), bg="#ffeb3b", command=get_hint).pack(pady=5)
        tk.Button(self.window, text="Quit Game", font=("Arial", 14, "bold"), bg="#ff6961", command=quit_game).pack(pady=5)

    # ---------------- HELPER FUNCTIONS ----------------
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def authenticate_user(self, username, password):
        with open(USERS_FILE, "r") as f:
            for line in f:
                stored_user, stored_pass = line.strip().split(",")
                if stored_user == username and stored_pass == password:
                    return True
        return False

    def register_user(self, username, password):
        with open(USERS_FILE, "r") as f:
            for line in f:
                stored_user, _ = line.strip().split(",")
                if stored_user == username:
                    return False
        with open(USERS_FILE, "a") as f:
            f.write(f"{username},{password}\n")
        return True
