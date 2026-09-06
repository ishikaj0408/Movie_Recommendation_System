import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os


# =====================================================
# MYSQL CONNECTION
# =====================================================

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
            "MySQL connection failed!\n\n"
            + str(error)
        )

        return None


# =====================================================
# GET USER DATA
# =====================================================

def get_user_data():

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT name, email
            FROM users
            ORDER BY id DESC
            LIMIT 1
            """
        )

        user = cursor.fetchone()

        if user:

            name_label.config(
                text=user[0]
            )

            email_label.config(
                text=user[1]
            )

        else:

            name_label.config(
                text="No user found"
            )

            email_label.config(
                text="No email found"
            )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )

    finally:

        cursor.close()
        connection.close()


# =====================================================
# GO HOME
# =====================================================

def go_home():

    root.destroy()

    home_file = os.path.join(
        os.path.dirname(__file__),
        "home.py"
    )

    subprocess.Popen(
        [sys.executable, home_file]
    )


# =====================================================
# LOGOUT
# =====================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:

        root.destroy()

        login_file = os.path.join(
            os.path.dirname(__file__),
            "login.py"
        )

        subprocess.Popen(
            [sys.executable, login_file]
        )


# =====================================================
# COLORS - COMMON PROJECT THEME
# =====================================================

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


# =====================================================
# MAIN WINDOW
# =====================================================

root = tk.Tk()

root.title(
    "My Profile - Movie Recommendation System"
)

root.state(
    "zoomed"
)

root.configure(
    bg=BG_COLOR
)


# =====================================================
# HEADER
# =====================================================

header = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    height=85
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# =====================================================
# HOME BUTTON
# =====================================================

home_button = tk.Button(
    header,
    text="←  HOME",
    font=("Segoe UI", 11, "bold"),
    bg=SIDEBAR_COLOR,
    fg=WHITE,
    activebackground=SIDEBAR_DARK,
    activeforeground=LIGHT_PURPLE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=go_home
)

home_button.pack(
    side="left",
    padx=30
)



tk.Label(
    header,
    text="MY PROFILE",
    font=("Segoe UI", 22, "bold"),
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    side="left"
)



logout_button = tk.Button(
    header,
    text="LOGOUT",
    font=("Segoe UI", 10, "bold"),
    bg=PURPLE,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    width=10,
    command=logout
)

logout_button.pack(
    side="right",
    padx=35,
    ipady=5
)


def logout_enter(event):

    logout_button.config(
        bg=LIGHT_PURPLE
    )


def logout_leave(event):

    logout_button.config(
        bg=PURPLE
    )


logout_button.bind(
    "<Enter>",
    logout_enter
)

logout_button.bind(
    "<Leave>",
    logout_leave
)



card = tk.Frame(
    root,
    bg=CARD_COLOR,
    width=550,
    height=500,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)



card.place(
    relx=0.5,
    rely=0.58,
    anchor="center"
)

card.pack_propagate(False)




tk.Frame(
    card,
    bg=PURPLE,
    height=5
).pack(
    fill="x"
)



tk.Label(
    card,
    text="👤",
    font=("Segoe UI Emoji", 50),
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    pady=(25, 5)
)



tk.Label(
    card,
    text="My Profile",
    font=("Segoe UI", 25, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack()


# =====================================================
# NAME TITLE
# =====================================================

tk.Label(
    card,
    text="NAME",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(30, 5)
)


# =====================================================
# NAME VALUE
# =====================================================

name_label = tk.Label(
    card,
    text="Loading...",
    font=("Segoe UI", 16, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

name_label.pack()


# =====================================================
# EMAIL TITLE
# =====================================================

tk.Label(
    card,
    text="EMAIL",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(22, 5)
)



email_label = tk.Label(
    card,
    text="Loading...",
    font=("Segoe UI", 16, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

email_label.pack()



tk.Label(
    card,
    text="MOVIE RECOMMENDATION SYSTEM",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    pady=(30, 0)
)



get_user_data()




root.mainloop()