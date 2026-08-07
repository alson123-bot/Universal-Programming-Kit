import sqlite3
from tkinter import *
from tkinter import ttk

# ================= DATABASE CONNECTION =================
conn = sqlite3.connect("ide_database.db")
cursor = conn.cursor()

# ================= CREATE TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    board TEXT,
    mode TEXT,
    timestamp TEXT
)
""")

conn.commit()

# ================= SAVE FUNCTION =================
def save_session(username, board, mode, timestamp):
    cursor.execute("""
        INSERT INTO user_sessions (username, board, mode, timestamp)
        VALUES (?, ?, ?, ?)
    """, (username, board, mode, timestamp))

    conn.commit()
    print("✔ DATA SAVED:", username, board, mode)


# ================= FETCH DATA =================
def fetch_data():
    cursor.execute("SELECT * FROM user_sessions")
    return cursor.fetchall()


# ================= GUI DATABASE VIEWER =================
def show_database_window():
    root = Tk()
    root.title("Database Viewer")
    root.geometry("850x450")

    # ================= BACKGROUND IMAGE =================
    bg_image = PhotoImage(file="abc.jpg")  # <-- put your image file here

    canvas = Canvas(root, width=850, height=450)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    # ================= TITLE =================
    canvas.create_text(
        425, 30,
        text="IDE USER DATABASE",
        font=("Segoe UI", 16, "bold"),
        fill="white"
    )

    # ================= FRAME FOR TABLE =================
    frame = Frame(root)
    frame.place(x=20, y=60, width=810, height=320)

    # ================= TABLE =================
    tree = ttk.Treeview(
        frame,
        columns=("ID", "User", "Board", "Mode", "Time"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("User", text="User")
    tree.heading("Board", text="Board")
    tree.heading("Mode", text="Mode")
    tree.heading("Time", text="Timestamp")

    tree.column("ID", width=50)
    tree.column("User", width=120)
    tree.column("Board", width=150)
    tree.column("Mode", width=100)
    tree.column("Time", width=200)

    tree.pack(fill="both", expand=True)

    # ================= LOAD DATA =================
    def load():
        for i in tree.get_children():
            tree.delete(i)

        for row in fetch_data():
            tree.insert("", "end", values=row)

    load()

    # ================= BUTTON =================
    Button(root, text="Refresh", command=load).place(x=400, y=390)

    # IMPORTANT: keep reference to image
    root.bg_image = bg_image

    root.mainloop()


# ================= RUN DIRECTLY =================
if __name__ == "__main__":
    show_database_window()