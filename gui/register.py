import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
import os


# =========================================================
# COLORS - SAME AS LOGIN.PY
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
# REGISTER USER
# =========================================================

def register_user():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get()
    confirm_password = confirm_entry.get()

    # =====================================================
    # EMPTY FIELD CHECK
    # =====================================================

    if (
        name == ""
        or email == ""
        or password == ""
        or confirm_password == ""
    ):

        messagebox.showwarning(
            "Missing Details",
            "Please fill all fields."
        )

        return


    # =====================================================
    # PASSWORD CHECK
    # =====================================================

    if password != confirm_password:

        messagebox.showerror(
            "Password Error",
            "Passwords do not match."
        )

        return


    # =====================================================
    # DATABASE CONNECTION
    # =====================================================

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    try:

        query = """
        INSERT INTO users
        (name, email, password)
        VALUES (%s, %s, %s)
        """

        values = (
            name,
            email,
            password
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        messagebox.showinfo(
            "Registration Successful",
            "Your account has been created successfully!"
        )

        root.destroy()

        login_file = os.path.join(
            os.path.dirname(__file__),
            "login.py"
        )

        subprocess.Popen(
            [sys.executable, login_file]
        )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Registration Failed",
            str(error)
        )

    finally:

        cursor.close()
        connection.close()


# =========================================================
# BACK TO LOGIN
# =========================================================

def back_to_login():

    root.destroy()

    login_file = os.path.join(
        os.path.dirname(__file__),
        "login.py"
    )

    subprocess.Popen(
        [sys.executable, login_file]
    )


# =========================================================
# SHOW / HIDE PASSWORD
# =========================================================

def show_password():

    if password_entry.cget("show") == "*":

        password_entry.config(
            show=""
        )

        password_button.config(
            text="HIDE"
        )

    else:

        password_entry.config(
            show="*"
        )

        password_button.config(
            text="SHOW"
        )


# =========================================================
# SHOW / HIDE CONFIRM PASSWORD
# =========================================================

def show_confirm_password():

    if confirm_entry.cget("show") == "*":

        confirm_entry.config(
            show=""
        )

        confirm_button.config(
            text="HIDE"
        )

    else:

        confirm_entry.config(
            show="*"
        )

        confirm_button.config(
            text="SHOW"
        )


# =========================================================
# BUTTON HOVER
# SAME STYLE AS LOGIN.PY
# =========================================================

def button_hover_enter(event):

    event.widget.config(
        bg=PURPLE
    )


def button_hover_leave(event):

    event.widget.config(
        bg=DARK_PURPLE
    )


# =========================================================
# SIMPLE LINK HOVER
# =========================================================

def link_hover_enter(event):

    event.widget.config(
        fg=DARK_PURPLE
    )


def link_hover_leave(event):

    event.widget.config(
        fg=PURPLE
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Create Account - Movie Recommendation System"
)

root.state(
    "zoomed"
)

root.configure(
    bg=BG_COLOR
)


# =========================================================
# MAIN FRAME
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
# TOP BAR
# =========================================================

top_bar = tk.Frame(
    main_frame,
    bg=BG_COLOR,
    height=80
)

top_bar.pack(
    fill="x"
)

top_bar.pack_propagate(False)


# =========================================================
# BACK TO LOGIN
# =========================================================

back_button = tk.Button(
    top_bar,
    text="←  BACK TO LOGIN",
    font=("Segoe UI", 10, "bold"),
    bg=DARK_PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=back_to_login
)

back_button.pack(
    side="left",
    padx=45,
    pady=25
)

back_button.bind(
    "<Enter>",
    button_hover_enter
)

back_button.bind(
    "<Leave>",
    button_hover_leave
)


# =========================================================
# PAGE BRAND
# =========================================================

tk.Label(
    top_bar,
    text="MOVIE RECOMMENDATION SYSTEM",
    font=("Segoe UI", 13, "bold"),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
).pack(
    side="right",
    padx=45
)


# =========================================================
# PAGE TITLE
# =========================================================




# =========================================================
# PAGE SUBTITLE
# =========================================================



# =========================================================
# REGISTER CARD
# =========================================================

card = tk.Frame(
    main_frame,
    bg=CARD_COLOR,
    width=570,
    height=555,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

card.pack()

card.pack_propagate(False)


# =========================================================
# CARD TITLE
# =========================================================

tk.Label(
    card,
    text="CREATE ACCOUNT",
    font=("Segoe UI", 23, "bold"),
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    pady=(28, 22)
)


# =========================================================
# FULL NAME LABEL
# =========================================================

tk.Label(
    card,
    text="FULL NAME",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# =========================================================
# NAME ENTRY
# =========================================================

name_entry = tk.Entry(
    card,
    font=("Segoe UI", 11, "bold"),
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=BLACK,
    relief="flat",
    bd=0
)

name_entry.pack(
    padx=55,
    fill="x",
    ipady=11,
    pady=(7, 18)
)


# =========================================================
# EMAIL LABEL
# =========================================================

tk.Label(
    card,
    text="EMAIL ADDRESS",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# =========================================================
# EMAIL ENTRY FRAME
# =========================================================

email_frame = tk.Frame(
    card,
    bg=ENTRY_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

email_frame.pack(
    padx=55,
    fill="x",
    pady=(7, 18)
)


# =========================================================
# EMAIL ICON
# =========================================================



# =========================================================
# EMAIL ENTRY
# =========================================================

email_entry = tk.Entry(
    email_frame,
    font=("Segoe UI", 11, "bold"),
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
    ipady=10,
    padx=(3, 10)
)


# =========================================================
# PASSWORD LABEL
# =========================================================

tk.Label(
    card,
    text="PASSWORD",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
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
    padx=55,
    fill="x",
    pady=(7, 18)
)


# =========================================================
# PASSWORD ICON
# =========================================================




# =========================================================
# PASSWORD ENTRY
# =========================================================

password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 11, "bold"),
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
    ipady=10
)


# =========================================================
# SHOW PASSWORD BUTTON
# =========================================================

password_button = tk.Button(
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

password_button.pack(
    side="right",
    padx=7,
    pady=5,
    ipadx=6,
    ipady=3
)


# =========================================================
# CONFIRM PASSWORD LABEL
# =========================================================

tk.Label(
    card,
    text="CONFIRM PASSWORD",
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=55
)


# =========================================================
# CONFIRM PASSWORD FRAME
# =========================================================

confirm_frame = tk.Frame(
    card,
    bg=ENTRY_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

confirm_frame.pack(
    padx=55,
    fill="x",
    pady=(7, 20)
)


# =========================================================
# CONFIRM PASSWORD ICON
# =========================================================




# =========================================================
# CONFIRM PASSWORD ENTRY
# =========================================================

confirm_entry = tk.Entry(
    confirm_frame,
    font=("Segoe UI", 11, "bold"),
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=BLACK,
    relief="flat",
    bd=0,
    show="*"
)

confirm_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10
)


# =========================================================
# SHOW CONFIRM PASSWORD BUTTON
# =========================================================

confirm_button = tk.Button(
    confirm_frame,
    text="SHOW",
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR_COLOR,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=show_confirm_password
)

confirm_button.pack(
    side="right",
    padx=7,
    pady=5,
    ipadx=6,
    ipady=3
)


# =========================================================
# CREATE ACCOUNT BUTTON
# =========================================================

register_button = tk.Button(
    card,
    text="CREATE ACCOUNT",
    font=("Segoe UI", 11, "bold"),
    bg=DARK_PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=register_user
)

register_button.pack(
    padx=55,
    fill="x",
    ipady=12
)


register_button.bind(
    "<Enter>",
    button_hover_enter
)

register_button.bind(
    "<Leave>",
    button_hover_leave
)


# =========================================================
# LOGIN TEXT
# =========================================================



# =========================================================
# BACK TO LOGIN BUTTON
# =========================================================


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: register_user()
)


# =========================================================
# INITIAL FOCUS
# =========================================================

name_entry.focus()


# =========================================================
# START
# =========================================================

root.mainloop()