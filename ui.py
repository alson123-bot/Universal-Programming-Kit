import serial
import time
import re
import threading
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from datetime import datetime

from database import save_session   #  IMPORTANT LINK

ser = None
user_name = ""


# ================= LEXICAL ANALYZER =================
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

        if kind in ['SKIP', 'NEWLINE']:
            continue
        tokens.append((kind, value))

    return tokens


# ================= ARDUINO SIMULATOR =================
class ArduinoSimulator:
    def __init__(self, output_box, result_label):
        self.output_box = output_box
        self.result_label = result_label

    def log(self, msg):
        self.output_box.insert(END, msg + "\n")
        self.output_box.see(END)

    def run(self, code):
        self.output_box.delete("1.0", END)

        tokens = lexical_analyzer(code)

        self.log("=== TOKENS ===")
        self.log(str(tokens))
        self.log("\n=== EXECUTION ===")

        code_low = code.lower()

        if "serial.print" in code_low:
            self.log("Serial Output Detected")

        if "pinmode" in code_low:
            self.log("Pin configured")

        if "digitalwrite" in code_low:
            if "high" in code_low:
                self.log("Pin set HIGH → LED ON")
                self.result_label.config(text="💡 The light is ON")
            elif "low" in code_low:
                self.log("Pin set LOW → LED OFF")
                self.result_label.config(text="💡 The light is OFF")

        if "delay" in code_low:
            self.log("Delay executed (simulated)")

        self.log("\n=== DONE ===")


# ================= CONNECT =================
def connect_device():
    global ser
    port = port_var.get()

    if not port or port == "Select Port":
        status_label.config(text="● Select a port first", fg="orange")
        return

    try:
        ser = serial.Serial(port, 9600, timeout=1)
        status_label.config(text=f"● Connected to {port}", fg="#00ff9c")
    except:
        status_label.config(text="● Connection Failed", fg="#ff4d4d")


# ================= SEND =================
def send_command(cmd):
    if ser and ser.is_open:
        ser.write((cmd + "\n").encode())
        time.sleep(0.5)
        response = ser.readline().decode().strip()
        output_label.config(text=response if response else "No response")
    else:
        output_label.config(text="Not connected")


# ================= START =================
def start_action():
    mode = mode_var.get()
    board = device_var.get()

    if board == "Select Board" or mode == "Select Mode":
        output_label.config(text="Please select board and mode")
        return

    save_session(
        user_name,
        board,
        mode,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    if mode == "Real":
        output_label.config(text="Any external device is not connected")

    elif mode == "Virtual":

        win = Toplevel(root)
        win.title(f"{board} Compiler")
        win.geometry("800x600")

        Label(
            win,
            text=f"{board} Compiler - {user_name}",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        text_area = ScrolledText(
            win,
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#00ff9c",
            insertbackground="white"
        )
        text_area.pack(fill="both", expand=True, padx=10, pady=5)

        text_area.insert("1.0", f"""// {board} Example
const int ledPin = 13;

void setup() {{
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
}}

void loop() {{
}}
""")

        output_box = ScrolledText(
            win,
            height=8,
            bg="black",
            fg="lime",
            font=("Consolas", 10)
        )
        output_box.pack(fill="both", padx=10, pady=5)

        result_label = Label(win, text="", font=("Segoe UI", 12), fg="dark blue")
        result_label.pack(pady=5)

        simulator = ArduinoSimulator(output_box, result_label)

        def run_code():
            code = text_area.get("1.0", END)
            threading.Thread(target=simulator.run, args=(code,)).start()

        Button(
            win,
            text="RUN",
            command=run_code,
            bg="#00aa00",
            fg="white",
            width=20,
            height=2
        ).pack(pady=5)


# ================= LOGIN =================
def open_main():
    global user_name

    user_name = name_entry.get()
    if user_name.strip() == "":
        return

    login.destroy()

    global root, device_var, mode_var, port_var
    global status_label, output_label
    global bg_main_image

    root = Tk()
    root.title("Universal Programming Kit")
    root.state("zoomed")

    # ================= MAIN BACKGROUND =================
    bg_main = Image.open("def.jpg")
    bg_main = bg_main.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_main_image = ImageTk.PhotoImage(bg_main)

    bg_label = Label(root, image=bg_main_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    frame = Frame(root, bg="#000000", width=900, height=600)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    Label(frame, text=f"Welcome {user_name}",
          font=("Segoe UI", 30, "bold"),
          bg="#000000", fg="white").pack(pady=10)

    device_var = StringVar(value="Select Board")
    ttk.Combobox(frame, textvariable=device_var,
                 values=["Select Board", "Arduino", "ESP32", "ESP8266", "Pico"],
                 state="readonly", width=40).pack(pady=5)

    mode_var = StringVar(value="Select Mode")
    ttk.Combobox(frame, textvariable=mode_var,
                 values=["Select Mode", "Real", "Virtual"],
                 state="readonly", width=40).pack(pady=5)

    port_var = StringVar(value="COM3")

    Button(frame, text="Connect", command=connect_device,
           bg="#2563eb", fg="white", width=30, height=2).pack(pady=8)

    Button(frame, text="START", command=start_action,
           bg="green", fg="white", width=30, height=2).pack(pady=8)

    Button(frame, text="STOP", command=lambda: send_command("OFF"),
           bg="red", fg="white", width=30, height=2).pack(pady=8)

    status_label = Label(frame, text="● Not Connected", bg="#000000", fg="white")
    status_label.pack(pady=5)

    output_label = Label(frame, text="", bg="#000000", fg="white")
    output_label.pack(pady=5)

    root.mainloop()


# ================= LOGIN WINDOW =================
login = Tk()
login.title("Login")
login.geometry("300x200")

# ================= LOGIN BACKGROUND =================
login_bg = Image.open("abc.jpg")
login_bg = login_bg.resize((300, 200))
login_bg_image = ImageTk.PhotoImage(login_bg)

login_bg_label = Label(login, image=login_bg_image)
login_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

Label(login, text="Enter Name",
      font=("Segoe UI", 14, "bold"), bg="black", fg="white").pack(pady=20)

name_entry = Entry(login, font=("Segoe UI", 12))
name_entry.pack(pady=10)

Button(login, text="Enter", command=open_main,
       bg="green", fg="white").pack(pady=10)

login.mainloop()