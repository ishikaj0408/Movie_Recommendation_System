import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys
import json


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "Data"
)
os.makedirs(
    DATA_DIR,exist_ok=True
)

FAVORITES_FILE = os.path.join(
    DATA_DIR,
    "favorites.json"
)



os.makedirs(
    DATA_DIR,
    exist_ok=True
)



BG_COLOR = "#F7F5FA"

SIDEBAR_COLOR = "#24113F"
BUTTON_COLOR = "#3D1068"

PURPLE = "#6D28D9"
LIGHT_PURPLE = "#A78BFA"
DARK_PURPLE = "#4C1D95"

CARD_COLOR = "#FFFFFF"

WHITE = "#FFFFFF"
BLACK = "#111111"

TEXT_COLOR = "#29212F"
SECONDARY_TEXT = "#746D7D"
MUTED_TEXT = "#A29AAE"
BORDER_COLOR = "#E5E0EA"

ENTRY_COLOR = "#F3F1F7"


SIDEBAR_TITLE_FONT = (
    "Segoe UI",
    23,
    "bold"
)

SIDEBAR_SUBTITLE_FONT = (
    "Segoe UI",
    11,
    "bold"
)

HEADER_FONT = (
    "Segoe UI",
    19,
    "bold"
)

TITLE_FONT = (
    "Segoe UI",
    28,
    "bold"
)

SUBTITLE_FONT = (
    "Segoe UI",
    11,
    "bold"
)

BUTTON_FONT = (
    "Segoe UI",
    10,
    "bold"
)

MOVIE_FONT = (
    "Segoe UI",
    14,
    "bold"
)



def load_favorites():

    if not os.path.exists(FAVORITES_FILE):

        return []

    try:

        with open(
            FAVORITES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):

                return data

            return []

    except Exception:

        return []



def save_favorites():

    try:

        with open(
            FAVORITES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                favorites,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            "Unable to save favorites.\n\n"
            + str(error)
        )



favorites = load_favorites()



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
        [
            sys.executable,
            file_path
        ]
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

    if os.path.exists(login_file):

        subprocess.Popen(
            [
                sys.executable,
                login_file
            ]
        )


# =========================================================
# SIDEBAR BUTTON
# =========================================================

def create_sidebar_button(
    text,
    command,
    active=False
):

    if active:

        button_color = PURPLE

    else:

        button_color = BUTTON_COLOR

    button = tk.Button(
        sidebar,
        text=text,
        font=BUTTON_FONT,
        bg=button_color,
        fg=WHITE,
        activebackground=button_color,
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

    return button



def update_count():

    count_label.config(
        text=f"{len(favorites)} MOVIES SAVED"
    )


def remove_favorite(movie):

    answer = messagebox.askyesno(
        "Remove Favorite",
        f"Remove '{movie}' from favorites?"
    )

    if not answer:

        return

    if movie in favorites:

        favorites.remove(movie)

        save_favorites()

    show_favorites(
        search_entry.get()
    )

    update_count()



def clear_all():

    if len(favorites) == 0:

        messagebox.showinfo(
            "Favorites",
            "Your favorites list is already empty."
        )

        return

    answer = messagebox.askyesno(
        "Clear Favorites",
        "Are you sure you want to remove all favorite movies?"
    )

    if not answer:

        return

    favorites.clear()

    save_favorites()

    show_favorites()

    update_count()



def search_favorites(event=None):

    show_favorites(
        search_entry.get()
    )



def show_favorites(search_text=""):


    for widget in favorites_container.winfo_children():

        widget.destroy()

    search_text = search_text.lower().strip()

    filtered_favorites = []

    for movie in favorites:

        movie_text = str(movie)

        if (
            search_text == ""
            or search_text in movie_text.lower()
        ):

            filtered_favorites.append(
                movie_text
            )


    if len(filtered_favorites) == 0:

        empty_card = tk.Frame(
            favorites_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        empty_card.pack(
            fill="x",
            padx=20,
            pady=25
        )

        tk.Label(
            empty_card,
            text="",
            font=("Segoe UI Emoji", 45),
            bg=CARD_COLOR,
            fg=PURPLE
        ).pack(
            pady=(30, 10)
        )

        if len(favorites) == 0:

            message = "No favorite movies yet."

            sub_message = (
                "Go to Movie Recommendation and "
                "add movies to your favorites."
            )

        else:

            message = "No movie found."

            sub_message = (
                "Try searching with another movie name."
            )

        tk.Label(
            empty_card,
            text=message,
            font=(
                "Segoe UI",
                17,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(
            pady=(0, 8)
        )

        tk.Label(
            empty_card,
            text=sub_message,
            font=SUBTITLE_FONT,
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            pady=(0, 30)
        )

        return

    # -----------------------------------------------------
    # MOVIE CARDS
    # -----------------------------------------------------

    for number, movie in enumerate(
        filtered_favorites,
        start=1
    ):

        movie_card = tk.Frame(
            favorites_container,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        movie_card.pack(
            fill="x",
            padx=20,
            pady=7
        )

        # -------------------------------------------------
        # PURPLE LINE
        # -------------------------------------------------

        tk.Frame(
            movie_card,
            bg=PURPLE,
            width=5
        ).pack(
            side="left",
            fill="y"
        )

        # -------------------------------------------------
        # NUMBER
        # -------------------------------------------------

        tk.Label(
            movie_card,
            text=f"{number:02d}",
            font=(
                "Segoe UI",
                13,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=PURPLE,
            width=5
        ).pack(
            side="left",
            padx=(12, 0),
            pady=18
        )

        # -------------------------------------------------
        # MOVIE ICON
        # -------------------------------------------------

        tk.Label(
            movie_card,
            text="🎬",
            font=("Segoe UI Emoji", 25),
            bg=CARD_COLOR
        ).pack(
            side="left",
            padx=10
        )

        # -------------------------------------------------
        # NAME FRAME
        # -------------------------------------------------

        name_frame = tk.Frame(
            movie_card,
            bg=CARD_COLOR
        )

        name_frame.pack(
            side="left",
            fill="x",
            expand=True,
            pady=14
        )

        # -------------------------------------------------
        # MOVIE NAME
        # -------------------------------------------------

        tk.Label(
            name_frame,
            text=movie,
            font=MOVIE_FONT,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            anchor="w"
        ).pack(
            anchor="w"
        )

        # -------------------------------------------------
        # SAVED TEXT
        # -------------------------------------------------

        tk.Label(
            name_frame,
            text="Saved in your favorites",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # -------------------------------------------------
        # REMOVE BUTTON
        # -------------------------------------------------

        tk.Button(
            movie_card,
            text="REMOVE  ♥",
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=BUTTON_COLOR,
            fg=WHITE,
            activebackground=DARK_PURPLE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda m=movie: remove_favorite(m)
        ).pack(
            side="right",
            padx=20,
            ipadx=10,
            ipady=7
        )




root = tk.Tk()

root.title(
    "Movie Recommendation System - My Favorites"
)

root.state(
    "zoomed"
)

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
    width=300
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(
    False
)



tk.Frame(
    sidebar,
    bg=LIGHT_PURPLE,
    height=5
).pack(
    fill="x"
)




tk.Label(
    sidebar,
    text="MOVIE",
    font=SIDEBAR_TITLE_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(50, 0)
)


tk.Label(
    sidebar,
    text="RECOMMENDATION",
    font=SIDEBAR_SUBTITLE_FONT,
    bg=SIDEBAR_COLOR,
    fg=LIGHT_PURPLE
).pack(
    pady=(3, 0)
)


tk.Label(
    sidebar,
    text="SYSTEM",
    font=SIDEBAR_SUBTITLE_FONT,
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(0, 35)
)


# =========================================================
# DIVIDER
# =========================================================

tk.Frame(
    sidebar,
    bg=LIGHT_PURPLE,
    height=1
).pack(
    fill="x",
    padx=28
)


# =========================================================
# MENU
# =========================================================

tk.Label(
    sidebar,
    text="MENU",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=SIDEBAR_COLOR,
    fg=MUTED_TEXT
).pack(
    anchor="w",
    padx=35,
    pady=(25, 10)
)


# =========================================================
# HOME
# =========================================================

create_sidebar_button(
    "HOME",
    lambda: open_page("home.py")
)


# =========================================================
# MOVIE RECOMMENDATION
# =========================================================

create_sidebar_button(
    "MOVIE RECOMMENDATION",
    lambda: open_page("recommendation.py")
)


# =========================================================
# MY FAVORITES
# =========================================================

create_sidebar_button(
    "MY FAVORITES  ❤️",
    lambda: None,
    active=True
)



create_sidebar_button(
    "MY PROFILE",
    lambda: open_page("profile.py")
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
    bg=LIGHT_PURPLE,
    height=1
).pack(
    fill="x",
    padx=28,
    pady=(0, 18)
)


 =========================================================

tk.Button(
    bottom_sidebar,
    text="LOGOUT",
    font=BUTTON_FONT,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_COLOR,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=logout
).pack(
    fill="x",
    padx=24,
    ipady=10
)


# =========================================================
# RIGHT AREA
# =========================================================

right_area = tk.Frame(
    main_container,
    bg=BG_COLOR
)

right_area.pack(
    side="right",
    fill="both",
    expand=True
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    right_area,
    bg=CARD_COLOR,
    height=72,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


tk.Label(
    header,
    text="MY FAVORITES  ❤️",
    font=HEADER_FONT,
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=40
)


# =========================================================
# HEADER STATUS
# =========================================================

status_frame = tk.Frame(
    header,
    bg=CARD_COLOR
)

status_frame.pack(
    side="right",
    padx=40
)


tk.Label(
    status_frame,
    text="●",
    font=("Arial", 10),
    bg=CARD_COLOR,
    fg=PURPLE
).pack(
    side="left",
    padx=(0, 7)
)


tk.Label(
    status_frame,
    text="YOUR PERSONAL MOVIE COLLECTION",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    side="left"
)


# =========================================================
# CONTENT
# =========================================================

content = tk.Frame(
    right_area,
    bg=BG_COLOR
)

content.pack(
    fill="both",
    expand=True,
    padx=45,
    pady=25
)


# =========================================================
# TITLE FRAME
# =========================================================

title_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

title_frame.pack(
    fill="x",
    padx=20
)


tk.Label(
    title_frame,
    text="Your Favorite Movies",
    font=TITLE_FONT,
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left"
)


# =========================================================
# COUNT
# =========================================================

count_label = tk.Label(
    title_frame,
    text="",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=PURPLE,
    fg=WHITE,
    padx=12,
    pady=6
)

count_label.pack(
    side="left",
    padx=18
)


# =========================================================
# CLEAR ALL
# =========================================================

tk.Button(
    title_frame,
    text="CLEAR ALL",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=clear_all
).pack(
    side="right",
    ipadx=12,
    ipady=6
)


# =========================================================
# SUBTITLE
# =========================================================

tk.Label(
    content,
    text="Movies you have saved for watching later.",
    font=SUBTITLE_FONT,
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
).pack(
    anchor="w",
    padx=20,
    pady=(3, 18)
)


# =========================================================
# SEARCH CARD
# =========================================================

search_card = tk.Frame(
    content,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

search_card.pack(
    fill="x",
    padx=20,
    pady=(0, 18)
)


tk.Label(
    search_card,
    text="SEARCH FAVORITES",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=(20, 10),
    pady=15
)


search_entry = tk.Entry(
    search_card,
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=PURPLE,
    relief="flat",
    bd=0,
    width=40
)

search_entry.pack(
    side="left",
    padx=5,
    pady=10,
    ipady=8
)


search_entry.bind(
    "<KeyRelease>",
    search_favorites
)


# =========================================================
# SEARCH BUTTON
# =========================================================

tk.Button(
    search_card,
    text="SEARCH",
    font=BUTTON_FONT,
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=search_favorites
).pack(
    side="left",
    padx=10,
    ipadx=12,
    ipady=7
)


# =========================================================
# FAVORITES FRAME
# =========================================================

favorites_frame = tk.Frame(
    content,
    bg=PURPLE,
    padx=2,
    pady=2
)

favorites_frame.pack(
    fill="both",
    expand=True,
    padx=20
)


# =========================================================
# CANVAS
# =========================================================

canvas = tk.Canvas(
    favorites_frame,
    bg=BG_COLOR,
    highlightthickness=0
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = tk.Scrollbar(
    favorites_frame,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


# =========================================================
# FAVORITES CONTAINER
# =========================================================

favorites_container = tk.Frame(
    canvas,
    bg=BG_COLOR
)


canvas_window = canvas.create_window(
    (0, 0),
    window=favorites_container,
    anchor="nw"
)


# =========================================================
# SCROLL REGION
# =========================================================

def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_canvas(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


favorites_container.bind(
    "<Configure>",
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_canvas
)


# =========================================================
# MOUSE WHEEL
# =========================================================

def mouse_wheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# =========================================================
# INITIAL DISPLAY
# =========================================================

update_count()

show_favorites()


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()