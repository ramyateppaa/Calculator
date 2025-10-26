# Advanced Scientific Calculator using Tkinter (Centered, Small Layout, Constrained Resize)
# ---------------------------------------------------------------------------------------
# This version starts with a small, centered window (400x600). It allows resizing
# but constrains the maximum size to 600x800 to prevent it from filling the screen.
# The window stays centered on the desktop even when resized, providing a balanced
# view on both phones and desktops. Elements scale proportionally within limits.

import tkinter as tk
from tkinter import messagebox
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Scientific Calculator")
        
        # Initial small size and center on screen
        window_width, window_height = 400, 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Allow resizing but set max size to keep it from filling the screen
        self.root.resizable(True, True)
        self.root.maxsize(600, 800)  # Maximum width and height
        self.root.minsize(350, 500)  # Minimum size for usability
        self.root.config(bg="#2E2E2E")  # Dark theme background
        self.dark_mode = True
        
        # Memory variable
        self.memory = 0
        
        # History list
        self.history = []
        
        # Entry widget for display (expands with window)
        self.display = tk.Entry(root, font=("Arial", 18), borderwidth=5, relief="ridge", justify="right", bg="#1E1E1E", fg="white")
        self.display.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=8, pady=10, padx=10, sticky="ew")
        
        # History display (expandable)
        self.history_label = tk.Label(root, text="History:", font=("Arial", 10), bg="#2E2E2E", fg="white")
        self.history_label.grid(row=1, column=0, columnspan=5, pady=5, sticky="w")
        self.history_text = tk.Text(root, height=4, width=40, bg="#1E1E1E", fg="white", state="disabled", wrap="word", font=("Arial", 10))
        self.history_text.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky="nsew")
        
        # Configure grid weights for responsiveness
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(2, weight=1)  # History expands
        
        # Button layout (scaled for smaller initial size)
        buttons = [
            ("7", "#4CAF50"), ("8", "#4CAF50"), ("9", "#4CAF50"), ("/", "#FF9800"), ("C", "#F44336"),
            ("4", "#4CAF50"), ("5", "#4CAF50"), ("6", "#4CAF50"), ("*", "#FF9800"), ("(", "#9C27B0"),
            ("1", "#4CAF50"), ("2", "#4CAF50"), ("3", "#4CAF50"), ("-", "#FF9800"), (")", "#9C27B0"),
            ("0", "#4CAF50"), (".", "#4CAF50"), ("=", "#2196F3"), ("+", "#FF9800"), ("sin", "#00BCD4"),
            ("cos", "#00BCD4"), ("tan", "#00BCD4"), ("log", "#00BCD4"), ("ln", "#00BCD4"), ("sqrt", "#00BCD4"),
            ("^", "#FF9800"), ("pi", "#9C27B0"), ("e", "#9C27B0"), ("MC", "#FFC107"), ("MR", "#FFC107"),
            ("MS", "#FFC107"), ("M+", "#FFC107"), ("Theme", "#607D8B")
        ]
        
        row_val, col_val = 3, 0
        for btn_text, color in buttons:
            btn = tk.Button(root, text=btn_text, font=("Arial", 12), height=2, width=5, bg=color, fg="white",
                            command=lambda t=btn_text: self.on_button_click(t))
            btn.grid(row=row_val, column=col_val, padx=3, pady=3, sticky="nsew")
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1
        
        # Bind keyboard for input
        self.root.bind("<Key>", self.on_key_press)
    
    def on_button_click(self, text):
        if text == "=":
            self.calculate()
        elif text == "C":
            self.display.delete(0, tk.END)
        elif text == "sin":
            self.display.insert(tk.END, "math.sin(")
        elif text == "cos":
            self.display.insert(tk.END, "math.cos(")
        elif text == "tan":
            self.display.insert(tk.END, "math.tan(")
        elif text == "log":
            self.display.insert(tk.END, "math.log10(")
        elif text == "ln":
            self.display.insert(tk.END, "math.log(")
        elif text == "sqrt":
            self.display.insert(tk.END, "math.sqrt(")
        elif text == "^":
            self.display.insert(tk.END, "**")
        elif text == "pi":
            self.display.insert(tk.END, str(math.pi))
        elif text == "e":
            self.display.insert(tk.END, str(math.e))
        elif text == "MC":
            self.memory = 0
        elif text == "MR":
            self.display.insert(tk.END, str(self.memory))
        elif text == "MS":
            try:
                self.memory = float(self.display.get())
            except:
                pass
        elif text == "M+":
            try:
                self.memory += float(self.display.get())
            except:
                pass
        elif text == "Theme":
            self.toggle_theme()
        else:
            self.display.insert(tk.END, text)
    
    def on_key_press(self, event):
        key = event.char
        if key in "0123456789+-*/.()":
            self.display.insert(tk.END, key)
        elif key == "\r":  # Enter key
            self.calculate()
        elif key == "\x08":  # Backspace
            self.display.delete(len(self.display.get())-1, tk.END)
    
    def calculate(self):
        try:
            expression = self.display.get()
            result = eval(expression, {"__builtins__": None}, {"math": math})
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.add_to_history(f"{expression} = {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
    
    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)
    
    def toggle_theme(self):
        if self.dark_mode:
            self.root.config(bg="white")
            self.display.config(bg="white", fg="black")
            self.history_label.config(bg="white", fg="black")
            self.history_text.config(bg="white", fg="black")
            self.dark_mode = False
        else:
            self.root.config(bg="#2E2E2E")
            self.display.config(bg="#1E1E1E", fg="white")
            self.history_label.config(bg="#2E2E2E", fg="white")
            self.history_text.config(bg="#1E1E1E", fg="white")
            self.dark_mode = True

# Run the calculator
if __name__ == "__main__":
    root = tk.Tk()
    calc = ScientificCalculator(root)
    root.mainloop()
