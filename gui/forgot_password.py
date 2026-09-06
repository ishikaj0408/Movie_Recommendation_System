import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
import subprocess
import sys


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
# FONTS
# =========================================================

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
            password="",
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
# RESET PASSWORD
# =========================================================

def reset_password():

    email = email_entry.get().strip()
    new_password = password_entry.get()
    confirm_password = confirm_entry.get()


    # =====================================================
    # EMPTY FIELDS
    # =====================================================

    if (
        email == ""
        or new_password == ""
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

    if new_password != confirm_password:

        messagebox.showerror(
            "Password Error",
            "Passwords do not match."
        )

        return


    # =====================================================
    # DATABASE
    # =====================================================

    connection = connect_database()

    if connection is None:
        return


    cursor = connection.cursor()


    try:

        # -------------------------------------------------
        # CHECK EMAIL
        # -------------------------------------------------

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()


        if user:

            # -------------------------------------------------
            # UPDATE PASSWORD
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE email = %s
                """,
                (
                    new_password,
                    email
                )
            )

            connection.commit()


            messagebox.showinfo(
                "Success",
                "Password changed successfully!"
            )


            root.destroy()


            # -------------------------------------------------
            # OPEN LOGIN
            # -------------------------------------------------

            login_file = os.path.join(
                os.path.dirname(__file__),
                "login.py"
            )

            subprocess.Popen(
                [sys.executable, login_file]
            )


        else:

            messagebox.showerror(
                "Account Not Found",
                "No account found with this email."
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
# SHOW / HIDE PASSWORD
# =========================================================

def show_password():

    if password_entry.cget("show") == "*":

        password_entry.config(
            show=""
        )

        password_show_button.config(
            text="HIDE"
        )

    else:

        password_entry.config(
            show="*"
        )

        password_show_button.config(
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

        confirm_show_button.config(
            text="HIDE"
        )

    else:

        confirm_entry.config(
            show="*"
        )

        confirm_show_button.config(
            text="SHOW"
        )


# =========================================================
# BUTTON HOVER
# =========================================================

def button_hover(
    button,
    normal_color,
    hover_color
):

    button.bind(
        "<Enter>",
        lambda event: button.config(
            bg=hover_color
        )
    )

    button.bind(
        "<Leave>",
        lambda event: button.config(
            bg=normal_color
        )
    )


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
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Forgot Password - Movie Recommendation System"
)

root.state(
    "zoomed"
)

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
# PAGE TITLE
# =========================================================


  




# =========================================================
# RESET CARD
# =========================================================

card = tk.Frame(
    main_frame,
    bg=CARD_COLOR,
    width=520,
    height=540,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

card.pack(
    pady=(80,0)
)
card.pack_propagate(False)


# =========================================================
# CARD TITLE
# =========================================================

tk.Label(
    card,
    text="RESET PASSWORD",
    font=CARD_TITLE,
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    pady=(32, 8)
)


tk.Label(
    card,
    text="Enter your email and create a new password",
    font=SMALL_FONT,
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
    fill="x",
    ipady=11,
    padx=12
)


# =========================================================
# NEW PASSWORD LABEL
# =========================================================

tk.Label(
    card,
    text="NEW PASSWORD",
    font=LABEL_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=60
)


# =========================================================
# NEW PASSWORD FRAME
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
    pady=(7, 18)
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
    ipady=11,
    padx=(12, 0)
)


password_show_button = tk.Button(
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

password_show_button.pack(
    side="right",
    padx=7,
    pady=5,
    ipadx=6,
    ipady=3
)

button_hover(
    password_show_button,
    SIDEBAR_COLOR,
    DARK_PURPLE
)


# =========================================================
# CONFIRM PASSWORD LABEL
# =========================================================

tk.Label(
    card,
    text="CONFIRM NEW PASSWORD",
    font=LABEL_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=60
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
    padx=60,
    fill="x",
    pady=(7, 25)
)


confirm_entry = tk.Entry(
    confirm_frame,
    font=ENTRY_FONT,
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
    ipady=11,
    padx=(12, 0)
)


confirm_show_button = tk.Button(
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

confirm_show_button.pack(
    side="right",
    padx=7,
    pady=5,
    ipadx=6,
    ipady=3
)

button_hover(
    confirm_show_button,
    SIDEBAR_COLOR,
    DARK_PURPLE
)


# =========================================================
# RESET PASSWORD BUTTON
# =========================================================

reset_button = tk.Button(
    card,
    text="RESET PASSWORD",
    font=BUTTON_FONT,
    bg=DARK_PURPLE,
    fg=WHITE,
    activebackground=PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=reset_password
)

reset_button.pack(
    padx=60,
    fill="x",
    ipady=12
)

button_hover(
    reset_button,
    DARK_PURPLE,
    PURPLE
)


# =========================================================
# BACK TO LOGIN
# =========================================================

tk.Button(
    card,
    text="BACK TO LOGIN",
    font=SMALL_FONT,
    bg=CARD_COLOR,
    fg=PURPLE,
    activebackground=CARD_COLOR,
    activeforeground=DARK_PURPLE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=back_to_login
).pack(
    pady=(18, 0)
)


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: reset_password()
)


# =========================================================
# INITIAL FOCUS
# =========================================================

email_entry.focus()


# =========================================================
# START
# =========================================================

root.mainloop()