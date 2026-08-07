# arduino_compiler.py
import tkinter as tk
from tkinter import scrolledtext
import re
import time
import threading


# ---------------- LEXICAL ANALYZER ---------------- #
def lexical_analyzer(code):
    tokens = []
    token_specification = [
        ('NUMBER',   r'\b\d+\b'),
        ('ID',       r'\b[A-Za-z_]\w*\b'),
        ('STRING',   r'\".*?\"'),
        ('OP',       r'[=;(),{}]'),
        ('SKIP',     r'[ \t]+'),
        ('NEWLINE',  r'\n'),
        ('MISMATCH', r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind in ['NUMBER', 'ID', 'STRING', 'OP']:
            tokens.append((kind, value))

    return tokens


# ---------------- SIMULATOR ---------------- #
class ArduinoSimulator:
    def __init__(self, output_box):
        self.output_box = output_box

    def log(self, msg):
        self.output_box.insert(tk.END, msg + "\n")
        self.output_box.see(tk.END)

    def run(self, code):
        tokens = lexical_analyzer(code)

        self.log("=== TOKENS ===")
        self.log(str(tokens))
        self.log("\n=== OUTPUT ===")

        if "digitalwrite" in code and "high" in code:
            self.log("💡 LED ON")
        elif "digitalwrite" in code and "low" in code:
            self.log("💡 LED OFF")
        elif "pinmode" in code:
            self.log("⚙️ Pin configured")
        else:
            self.log("⚠️ Cannot simulate")


# ---------------- GUI WINDOW FUNCTION ---------------- #
def open_compiler_window():
    win = tk.Tk()
    win.title("Arduino Compiler (Virtual)")
    win.geometry("800x600")

    text = scrolledtext.ScrolledText(win, height=20)
    text.pack(fill=tk.BOTH, padx=10, pady=10)

    output = scrolledtext.ScrolledText(win, height=15, bg="black", fg="lime")
    output.pack(fill=tk.BOTH, padx=10, pady=10)

    sim = ArduinoSimulator(output)

    def run_code():
        code = text.get("1.0", tk.END)
        output.delete("1.0", tk.END)
        threading.Thread(target=sim.run, args=(code,)).start()

    tk.Button(win, text="RUN", bg="green", fg="white", command=run_code).pack()

    win.mainloop()