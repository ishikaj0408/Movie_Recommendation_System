import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F7F5FA"

SIDEBAR_COLOR = "#24113F"
SIDEBAR_DARK = "#190C2D"

HEADER_COLOR = "#FFFFFF"

CARD_COLOR = "#FFFFFF"
CARD_HOVER = "#F3EFF8"
LIGHT_PURPLE="#A78BFA"
# SAME COLORS AS LOGIN BUTTON
PURPLE = "#6D28D9"
PURPLE_HOVER = "#7C3AED"
PURPLE_DARK = "#4C1D95"

WHITE = "#FFFFFF"
BLACK = "#111111"

TEXT_COLOR = "#29212F"
SECONDARY_TEXT = "#746D7D"
MUTED_TEXT = "#A29AAE"

BORDER_COLOR = "#E5E0EA"


# =========================================================
# FONTS
# =========================================================

SIDEBAR_TITLE = ("Segoe UI", 23, "bold")
SIDEBAR_SUBTITLE = ("Segoe UI", 11, "bold")

HEADER_FONT = ("Segoe UI", 19, "bold")

HERO_SMALL = ("Segoe UI", 11, "bold")
HERO_TITLE = ("Segoe UI", 32, "bold")
HERO_TEXT = ("Segoe UI", 11)

CARD_TITLE = ("Segoe UI", 16, "bold")
CARD_TEXT = ("Segoe UI", 10)

BUTTON_FONT = ("Segoe UI", 10, "bold")
SMALL_FONT = ("Segoe UI", 9, "bold")



def open_page(file_name):

    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )

    if not os.path.exists(file_path):

        messagebox.showerror(
            "Page Not Found",
            file_name + " was not found."
        )

        return

    root.destroy()

    subprocess.Popen(
        [sys.executable, file_path]
    )



def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if not answer:
        return

    root.destroy()

    login_file = os.path.join(
        os.path.dirname(__file__),
        "login.py"
    )

    subprocess.Popen(
        [sys.executable, login_file]
    )



def add_hover(
    button,
    normal_color,
    hover_color
):

    def mouse_enter(event):

        button.config(
            bg=hover_color
        )

    def mouse_leave(event):

        button.config(
            bg=normal_color
        )

    button.bind(
        "<Enter>",
        mouse_enter
    )

    button.bind(
        "<Leave>",
        mouse_leave
    )



root = tk.Tk()

root.title(
    "Movie Recommendation System"
)

root.state("zoomed")

root.configure(
    bg=BG_COLOR
)



main_container = tk.Frame(
    root,
    bg=BG_COLOR
)

main_container.pack(
    fill="both",
    expand=True
)


sidebar = tk.Frame(
    main_container,
    bg=SIDEBAR_COLOR,
    width=320
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)



tk.Frame(
    sidebar,
    bg=PURPLE,
    height=5
).pack(
    fill="x"
)



tk.Label(
    sidebar,
    text="MOVIE",
    font=SIDEBAR_TITLE,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(50, 0)
)


tk.Label(
    sidebar,
    text="RECOMMENDATION",
    font=SIDEBAR_SUBTITLE,
    bg=SIDEBAR_COLOR,
    fg=PURPLE
).pack(
    pady=(3, 0)
)


tk.Label(
    sidebar,
    text="SYSTEM",
    font=SIDEBAR_SUBTITLE,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(0, 35)
)



tk.Frame(
    sidebar,
    bg="#3A2A4A",
    height=1
).pack(
    fill="x",
    padx=28
)



tk.Label(
    sidebar,
    text="MENU",
    font=("Segoe UI", 9, "bold"),
    bg=SIDEBAR_COLOR,
    fg=MUTED_TEXT
).pack(
    anchor="w",
    padx=35,
    pady=(25, 10)
)



def create_sidebar_button(
    text,
    command,
    active=False
):

    # LOGIN PAGE BUTTON COLOR
    if active:

        bg_color = PURPLE_DARK

    else:

        bg_color = "#241334"


    button = tk.Button(
        sidebar,
        text=text,
        font=BUTTON_FONT,
        bg=bg_color,
        fg=WHITE,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        anchor="w",
        padx=22,
        command=command
    )

    button.pack(
        fill="x",
        padx=24,
        pady=6,
        ipady=11
    )


    if not active:

        add_hover(
            button,
            "#241334",
            PURPLE_DARK
        )


    return button




create_sidebar_button(
    "HOME",
    lambda: None,
    active=True
)


create_sidebar_button(
    "MOVIE RECOMMENDATION",
    lambda: open_page(
        "recommendation.py"
    )
)


create_sidebar_button(
    "MY PROFILE",
    lambda: open_page(
        "profile.py"
    )
)







bottom_sidebar = tk.Frame(
    sidebar,
    bg=SIDEBAR_COLOR
)

bottom_sidebar.pack(
    side="bottom",
    fill="x",
    pady=25
)


tk.Frame(
    bottom_sidebar,
    bg="#3A2A4A",
    height=1
).pack(
    fill="x",
    padx=28,
    pady=(0, 18)
)




logout_button = tk.Button(
    bottom_sidebar,
    text="LOGOUT",
    font=BUTTON_FONT,

    # SAME AS LOGIN BUTTON
    bg=PURPLE_DARK,

    fg=WHITE,

    activebackground=PURPLE,
    activeforeground=WHITE,

    relief="flat",
    bd=0,
    cursor="hand2",
    command=logout
)

logout_button.pack(
    fill="x",
    padx=24,
    ipady=10
)


add_hover(
    logout_button,
    PURPLE_DARK,
    PURPLE
)


right_area = tk.Frame(
    main_container,
    bg=BG_COLOR
)

right_area.pack(
    side="right",
    fill="both",
    expand=True
)



header = tk.Frame(
    right_area,
    bg=HEADER_COLOR,
    height=72,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


tk.Label(
    header,
    text="MOVIE RECOMMENDATION",
    font=HEADER_FONT,
    bg=HEADER_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=40
)



status_frame = tk.Frame(
    header,
    bg=HEADER_COLOR
)

status_frame.pack(
    side="right",
    padx=40
)


tk.Label(
    status_frame,
    text="●",
    font=("Arial", 10),
    bg=HEADER_COLOR,
    fg=PURPLE
).pack(
    side="left",
    padx=(0, 7)
)


tk.Label(
    status_frame,
    text="SYSTEM READY",
    font=SMALL_FONT,
    bg=HEADER_COLOR,
    fg=SECONDARY_TEXT
).pack(
    side="left"
)



hero = tk.Frame(
    right_area,
    bg="#FFFFFF",
    height=235,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

hero.pack(
    fill="x",
    padx=45,
    pady=(30, 0)
)

hero.pack_propagate(False)



hero_left = tk.Frame(
    hero,
    bg="#FFFFFF"
)

hero_left.pack(
    side="left",
    padx=45,
    pady=30
)


tk.Label(
    hero_left,
    text="WELCOME TO YOUR",
    font=HERO_SMALL,
    bg="#FFFFFF",
    fg=PURPLE
).pack(
    anchor="w"
)


tk.Label(
    hero_left,
    text="MOVIE WORLD",
    font=HERO_TITLE,
    bg="#FFFFFF",
    fg=TEXT_COLOR
).pack(
    anchor="w",
    pady=(3, 5)
)


tk.Label(
    hero_left,
    text="Discover movies that match your taste",
    font=HERO_TEXT,
    bg="#FFFFFF",
    fg=SECONDARY_TEXT
).pack(
    anchor="w"
)



start_button = tk.Button(
    hero_left,
    text="START EXPLORING  →",
    font=BUTTON_FONT,

    bg=PURPLE_DARK,

    fg=WHITE,

    activebackground=PURPLE,
    activeforeground=WHITE,

    relief="flat",
    bd=0,
    cursor="hand2",

    command=lambda: open_page(
        "recommendation.py"
    )
)

start_button.pack(
    anchor="w",
    pady=(15, 0),
    ipadx=16,
    ipady=7
)


add_hover(
    start_button,
    PURPLE_DARK,
    PURPLE
)



hero_right = tk.Frame(
    hero,
    bg="#FFFFFF",
    width=250
)

hero_right.pack(
    side="right",
    fill="y",
    padx=45
)

hero_right.pack_propagate(False)


tk.Label(
    hero_right,
    text="🎬",
    font=("Segoe UI Emoji", 68),
    bg="#FFFFFF",
    fg=PURPLE
).pack(
    pady=(35, 0)
)


tk.Label(
    hero_right,
    text="DISCOVER • EXPLORE • ENJOY",
    font=("Segoe UI", 8, "bold"),
    bg="#FFFFFF",
    fg=MUTED_TEXT
).pack()



quick_title = tk.Frame(
    right_area,
    bg=BG_COLOR
)

quick_title.pack(
    fill="x",
    padx=55,
    pady=(30, 12)
)


tk.Label(
    quick_title,
    text="QUICK ACCESS",
    font=("Segoe UI", 15, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left"
)


tk.Label(
    quick_title,
    text="Choose an option to continue",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=MUTED_TEXT
).pack(
    side="right"
)


cards_frame = tk.Frame(
    right_area,
    bg=BG_COLOR
)

cards_frame.pack(
    fill="x",
    padx=75
)


def create_card(
    title,
    description,
    button_text,
    command,
    column
):

    card = tk.Frame(
        cards_frame,
        bg=CARD_COLOR,
        width=330,
        height=225,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=column,
        padx=35
    )

    card.grid_propagate(False)


    # TOP ACCENT

    tk.Frame(
        card,
        bg=PURPLE,
        height=4
    ).pack(
        fill="x"
    )


    # TITLE

    tk.Label(
        card,
        text=title,
        font=CARD_TITLE,
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    ).pack(
        pady=(30, 10)
    )


    # DESCRIPTION

    tk.Label(
        card,
        text=description,
        font=CARD_TEXT,
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT,
        wraplength=260,
        justify="center"
    ).pack(
        padx=25
    )



    button = tk.Button(
        card,
        text=button_text,
        font=BUTTON_FONT,

        bg=PURPLE_DARK,

        fg=WHITE,

        activebackground=PURPLE,
        activeforeground=WHITE,

        relief="flat",
        bd=0,
        cursor="hand2",
        width=18,

        command=command
    )

    button.pack(
        pady=20,
        ipady=7
    )


    add_hover(
        button,
        PURPLE_DARK,
        PURPLE
    )



create_card(
    "MOVIE RECOMMENDATION",
    "Select a movie and discover movies similar to your choice.",
    "START",
    lambda: open_page(
        "recommendation.py"
    ),
    0
)



create_card(
    "MY PROFILE",
    "View your account details and personal information.",
    "VIEW PROFILE",
    lambda: open_page(
        "profile.py"
    ),
    1
)


info_box = tk.Frame(
    right_area,
    bg=SIDEBAR_COLOR,
    height=72
)

info_box.pack(
    fill="x",
    padx=100,
    pady=(32, 0)
)

info_box.pack_propagate(False)


tk.Label(
    info_box,
    text="SMART MOVIE DISCOVERY",
    font=("Segoe UI", 11, "bold"),
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(14, 3)
)


tk.Label(
    info_box,
    text=(
        "SELECT MOVIE   •   ANALYZE   •   "
        "FIND SIMILAR MOVIES   •   RECOMMEND"
    ),
    font=("Segoe UI", 8, "bold"),
    bg=SIDEBAR_COLOR,
    fg=LIGHT_PURPLE
).pack()


root.mainloop()