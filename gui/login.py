import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import subprocess
import sys


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F7F5FA"

SIDEBAR_COLOR = "#24113F"
SIDEBAR_DARK = "#190C2D"

PURPLE = "#6D28D9"
LIGHT_PURPLE = "#A78BFA"
DARK_PURPLE = "#4C1D95"

CARD_COLOR = "#FFFFFF"
ENTRY_COLOR = "#F3F1F7"

BLACK = "#111111"
WHITE = "#FFFFFF"
TEXT_COLOR = "#29212F"
SECONDARY_TEXT = "#746D7D"
MUTED_TEXT = "#A29AAE"
BORDER_COLOR = "#E5E0EA"


# =========================================================
# FONTS
# =========================================================

BRAND_FONT = ("Segoe UI", 30, "bold")
BRAND_SMALL = ("Segoe UI", 15, "bold")

QUOTE_FONT = ("Segoe UI", 18, "bold")
QUOTE_SMALL = ("Segoe UI", 10, "bold")

TITLE_FONT = ("Segoe UI", 30, "bold")
SUBTITLE_FONT = ("Segoe UI", 11, "bold")

CARD_TITLE = ("Segoe UI", 23, "bold")

LABEL_FONT = ("Segoe UI", 10, "bold")
ENTRY_FONT = ("Segoe UI", 11, "bold")
BUTTON_FONT = ("Segoe UI", 11, "bold")
SMALL_FONT = ("Segoe UI", 9, "bold")


# =========================================================
# MYSQL CONNECTION
# =========================================================

def connect_database():

    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Ishika@123",
            database="movie_recommendation"
        )

        return connection

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            "MySQL connection failed!\n\n" + str(error)
        )

        return None


# =========================================================
# LOGIN
# =========================================================

def login_user():

    email = email_entry.get().strip()
    password = password_entry.get()

    if email == "" or password == "":

        messagebox.showwarning(
            "Missing Details",
            "Please enter email and password."
        )

        return

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:

        query = """
        SELECT name
        FROM users
        WHERE email = %s AND password = %s
        """

        cursor.execute(
            query,
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            messagebox.showinfo(
                "Login Successful",
                "Welcome " + user[0] + "!"
            )

            root.destroy()

            home_file = os.path.join(
                os.path.dirname(__file__),
                "home.py"
            )

            subprocess.Popen(
                [sys.executable, home_file]
            )

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Error",
            str(error)
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# OPEN REGISTER
# =========================================================

def open_register():

    root.destroy()

    register_file = os.path.join(
        os.path.dirname(__file__),
        "register.py"
    )

    subprocess.Popen(
        [sys.executable, register_file]
    )


# =========================================================
# OPEN FORGOT PASSWORD
# =========================================================

def open_forgot_password():

    root.destroy()

    forgot_file = os.path.join(
        os.path.dirname(__file__),
        "forgot_password.py"
    )

    subprocess.Popen(
        [sys.executable, forgot_file]
    )


# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def show_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")
        show_button.config(text="HIDE")

    else:

        password_entry.config(show="*")
        show_button.config(text="SHOW")


# =========================================================
# LOGIN BUTTON HOVER
# =========================================================

def login_hover_enter(event):

    login_button.config(
        bg=DARK_PURPLE
    )


def login_hover_leave(event):

    login_button.config(
        bg=PURPLE
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Movie Recommendation System"
)

root.state("zoomed")

root.configure(
    bg=BG_COLOR
)


# =========================================================
# MAIN CONTAINER
# =========================================================

main_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# LARGE SIDEBAR
# =========================================================

sidebar = tk.Frame(
    main_frame,
    bg=SIDEBAR_COLOR,
    width=700
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# =========================================================
# TOP DECORATION
# =========================================================

tk.Frame(
    sidebar,
    bg=LIGHT_PURPLE,
    height=5
).pack(
    fill="x"
)


# =========================================================
# MOVIE ICON
# =========================================================

tk.Label(
    sidebar,
    text="🎬",
    font=("Segoe UI Emoji", 62),
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(75, 20)
)


# =========================================================
# MOVIE
# =========================================================

tk.Label(
    sidebar,
    text="MOVIE",
    font=BRAND_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack()


# =========================================================
# RECOMMENDATION
# =========================================================

tk.Label(
    sidebar,
    text="RECOMMENDATION",
    font=BRAND_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(3, 0)
)


# =========================================================
# SYSTEM
# =========================================================

tk.Label(
    sidebar,
    text="SYSTEM",
    font=BRAND_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(0, 55)
)


# =========================================================
# DIVIDER
# =========================================================

tk.Frame(
    sidebar,
    bg=LIGHT_PURPLE,
    height=2,
    width=230
).pack(
    pady=(0, 45)
)


# =========================================================
# QUOTE MARK
# =========================================================




# =========================================================
# QUOTE
# =========================================================

tk.Label(
    sidebar,
    text=(
        "Every movie has a story."
        "Let us help you\n"
        "find yours."
    ),
    font=QUOTE_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE,
    justify="center"
).pack(
    pady=(0, 25)
)


# =========================================================
# SMALL QUOTE TEXT
# =========================================================

tk.Label(
    sidebar,
    text="DISCOVER  •  EXPLORE  •  RECOMMEND",
    font=QUOTE_SMALL,
    bg=SIDEBAR_COLOR,
    fg=LIGHT_PURPLE
).pack()


# =========================================================
# DESCRIPTION
# =========================================================

tk.Label(
    sidebar,
    text=(
        "Your personalized movie journey\n"
        "starts with a single choice."
    ),
    font=("Segoe UI", 11, "bold"),
    bg=SIDEBAR_COLOR,
    fg="#B8AFC4",
    justify="center"
).pack(
    pady=(30, 0)
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    sidebar,
    text="MOVIE RECOMMENDATION SYSTEM  •  2026",
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR_COLOR,
    fg="#786B87"
).pack(
    side="bottom",
    pady=30
)


# =========================================================
# RIGHT AREA
# =========================================================

right_area = tk.Frame(
    main_frame,
    bg=BG_COLOR
  
)

right_area.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================================================
# WELCOME
# =========================================================

welcome_frame = tk.Frame(
    right_area,
    bg=BG_COLOR
)

welcome_frame.pack(
    pady=(75, 30)
)


tk.Label(
    welcome_frame,
    text="Welcome Back!",
    font=TITLE_FONT,
    bg=BG_COLOR,
    fg=BLACK
).pack()


tk.Label(
    welcome_frame,
    text="Sign in to continue your movie journey",
    font=SUBTITLE_FONT,
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(8, 0)
)


# =========================================================
# LOGIN CARD
# =========================================================

card = tk.Frame(
    right_area,
    bg=CARD_COLOR,
    width=520,
    height=475,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

card.place(
    relx=0.55,
    rely=0.57,
    anchor="center"
)

card.pack_propagate(False)


# =========================================================
# CARD TITLE
# =========================================================

tk.Label(
    card,
    text="LOGIN",
    font=CARD_TITLE,
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    pady=(32, 8)
)


tk.Label(
    card,
    text="Enter your account details",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(0, 25)
)


# =========================================================
# EMAIL LABEL
# =========================================================

tk.Label(
    card,
    text="EMAIL ADDRESS",
    font=LABEL_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=60
)


# =========================================================
# EMAIL ENTRY
# =========================================================

email_frame = tk.Frame(
    card,
    bg=ENTRY_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

email_frame.pack(
    padx=60,
    fill="x",
    pady=(7, 18)
)


tk.Label(
    email_frame,

    font=("Segoe UI", 13, "bold"),
    bg=ENTRY_COLOR,
    fg=PURPLE
).pack(
    side="left",
    padx=(12, 5)
)


email_entry = tk.Entry(
    email_frame,
    font=ENTRY_FONT,
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=BLACK,
    relief="flat",
    bd=0
)

email_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11,
    padx=(3, 10)
)


# =========================================================
# PASSWORD LABEL
# =========================================================

tk.Label(
    card,
    text="PASSWORD",
    font=LABEL_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=60
)


# =========================================================
# PASSWORD FRAME
# =========================================================

password_frame = tk.Frame(
    card,
    bg=ENTRY_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

password_frame.pack(
    padx=60,
    fill="x",
    pady=(7, 8)
)


tk.Label(
    password_frame,
  
    font=("Segoe UI Emoji", 11),
    bg=ENTRY_COLOR,
    fg=PURPLE
).pack(
    side="left",
    padx=(12, 5)
)


password_entry = tk.Entry(
    password_frame,
    font=ENTRY_FONT,
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=BLACK,
    relief="flat",
    bd=0,
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11
)


# =========================================================
# SHOW PASSWORD
# =========================================================

show_button = tk.Button(
    password_frame,
    text="SHOW",
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR_COLOR,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=show_password
)

show_button.pack(
    side="right",
    padx=7,
    pady=5,
    ipadx=6,
    ipady=3
)


# =========================================================
# FORGOT PASSWORD
# =========================================================

tk.Button(
    card,
    text="Forgot Password?",
    font=SMALL_FONT,
    bg=CARD_COLOR,
    fg=PURPLE,
    activebackground=CARD_COLOR,
    activeforeground=DARK_PURPLE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_forgot_password
).pack(
    anchor="e",
    padx=60,
    pady=(2, 18)
)


# =========================================================
# LOGIN BUTTON
# =========================================================

login_button = tk.Button(
    card,
    text="LOGIN",
    font=BUTTON_FONT,
    bg=DARK_PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=PURPLE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=login_user
)

login_button.pack(
    padx=60,
    fill="x",
    ipady=12
)


login_button.bind(
    "<Enter>",
    login_hover_enter
)

login_button.bind(
    "<Leave>",
    login_hover_leave
)


# =========================================================
# CREATE ACCOUNT
# =========================================================

create_frame = tk.Frame(
    card,
    bg=CARD_COLOR
)

create_frame.pack(
    pady=(20, 0)
)


tk.Label(
    create_frame,
    text="Don't have an account?",
    font=SMALL_FONT,
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    side="left"
)


tk.Button(
    create_frame,
    text=" CREATE ACCOUNT",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_COLOR,
    fg=PURPLE,
    activebackground=CARD_COLOR,
    activeforeground=DARK_PURPLE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=open_register
).pack(
    side="left"
)


# =========================================================
# BOTTOM TEXT
# =========================================================




# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: login_user()
)


# =========================================================
# EMAIL FOCUS
# =========================================================

email_entry.focus()


# =========================================================
# START
# =========================================================

root.mainloop()