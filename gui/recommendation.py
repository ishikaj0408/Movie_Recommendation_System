import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pickle
import os
import json
import ast
import re
import numpy as np


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "Model"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "Data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

FAVORITES_FILE = os.path.join(
    DATA_DIR,
    "favorites.json"
)


# =========================================================
# MODEL FILES
# =========================================================

KNN_FILE = os.path.join(
    MODEL_DIR,
    "knn_model.pkl"
)

MOVIES_FILE = os.path.join(
    MODEL_DIR,
    "movies.pkl"
)

SCALER_FILE = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

try:

    with open(
        KNN_FILE,
        "rb"
    ) as file:

        knn_model = pickle.load(
            file
        )


    movies = pd.read_pickle(
        MOVIES_FILE
    )


    with open(
        SCALER_FILE,
        "rb"
    ) as file:

        knn_scaler = pickle.load(
            file
        )


except Exception as error:

    messagebox.showerror(
        "Model Error",
        "Unable to load recommendation model.\n\n"
        + str(error)
        + "\n\n"
        "Please run Training.py again."
    )

    raise SystemExit


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#F7F5FA"
SIDEBAR_COLOR = "#24113F"
BUTTON_COLOR = "#3D1068"
PURPLE = "#6D28D9"
DARK_PURPLE = "#4C1D95"
LIGHT_PURPLE = "#A78BFA"

CARD_COLOR = "#FFFFFF"
ENTRY_COLOR = "#F3F1F7"

TEXT_COLOR = "#29212F"
SECONDARY_TEXT = "#746D7D"
MUTED_TEXT = "#A29AAE"
BORDER_COLOR = "#E5E0EA"

WHITE = "#FFFFFF"
BLACK = "#111111"


# =========================================================
# FIND COLUMN
# =========================================================

def find_column(names):

    lower_columns = {
        str(column).lower().strip():
        column
        for column in movies.columns
    }

    for name in names:

        key = str(
            name
        ).lower().strip()

        if key in lower_columns:

            return lower_columns[key]

    return None


# =========================================================
# DETECT COLUMNS
# =========================================================

title_column = find_column([
    "title",
    "movie title",
    "movie_title",
    "name"
])

genre_column = find_column([
    "genres",
    "genre"
])

rating_column = find_column([
    "rating",
    "ratings",
    "vote_average",
    "imdb_rating"
])

year_column = find_column([
    "year",
    "release_year",
    "release year",
    "release_date"
])

language_cinema_column = find_column([
    "language_cinema",
    "language cinema",
    "cinema"
])

languages_column = find_column([
    "languages",
    "language",
    "original_language"
])


# =========================================================
# TITLE CHECK
# =========================================================

if title_column is None:

    messagebox.showerror(
        "Dataset Error",
        "Movie title column was not found."
    )

    raise SystemExit


# =========================================================
# CHECK TRAINING FEATURES
# =========================================================

required_features = [
    "year",
    "rating",
    "genre_count",
    "language_count",
    "genre_encoded",
    "language_encoded",
    "language_cinema_encoded"
]


missing_features = [
    feature
    for feature in required_features
    if feature not in movies.columns
]


if missing_features:

    messagebox.showerror(
        "Model Data Error",
        "Required trained features are missing:\n\n"
        + "\n".join(missing_features)
        + "\n\n"
        "Please run Training.py again."
    )

    raise SystemExit


# =========================================================
# CLEAN GENRE
# =========================================================

def clean_genre(value):

    if pd.isna(value):

        return "Not Available"


    text = str(
        value
    ).strip()


    if not text:

        return "Not Available"


    genres = []


    # -----------------------------------------------------
    # LIST / DICTIONARY
    # -----------------------------------------------------

    try:

        parsed = ast.literal_eval(
            text
        )


        if isinstance(
            parsed,
            list
        ):

            for item in parsed:

                if isinstance(
                    item,
                    dict
                ):

                    name = item.get(
                        "name"
                    )

                    if name:

                        genres.append(
                            str(name).strip()
                        )


                elif isinstance(
                    item,
                    str
                ):

                    genres.append(
                        item.strip()
                    )


        elif isinstance(
            parsed,
            dict
        ):

            name = parsed.get(
                "name"
            )

            if name:

                genres.append(
                    str(name).strip()
                )


    except Exception:

        pass


    # -----------------------------------------------------
    # TMDB FORMAT
    # -----------------------------------------------------

    if not genres:

        matches = re.findall(
            r"""['"]name['"]\s*:\s*['"]([^'"]+)['"]""",
            text
        )

        genres.extend(
            matches
        )


    # -----------------------------------------------------
    # NORMAL TEXT
    # -----------------------------------------------------

    if not genres:

        text = re.sub(
            r"\bid\s*:\s*\d+",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\bname\s*:",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"[\[\]\{\}'\"]",
            "",
            text
        )

        parts = re.split(
            r"[,|;/]+",
            text
        )

        genres.extend(
            parts
        )


    # -----------------------------------------------------
    # UNIQUE
    # -----------------------------------------------------

    final_genres = []

    seen = set()


    for genre in genres:

        genre = str(
            genre
        ).strip()


        if not genre:

            continue


        if genre.lower() in [
            "nan",
            "none",
            "null"
        ]:

            continue


        key = genre.lower()


        if key not in seen:

            seen.add(
                key
            )

            final_genres.append(
                genre
            )


    if final_genres:

        return ", ".join(
            final_genres
        )


    return "Not Available"


# =========================================================
# CLEAN LANGUAGE
# =========================================================

def clean_language(value):

    if pd.isna(value):

        return ""


    text = str(
        value
    ).strip()


    if not text:

        return ""


    try:

        parsed = ast.literal_eval(
            text
        )

        values = []


        if isinstance(
            parsed,
            list
        ):

            for item in parsed:

                if isinstance(
                    item,
                    dict
                ):

                    for key in [
                        "name",
                        "language"
                    ]:

                        if item.get(
                            key
                        ):

                            values.append(
                                str(
                                    item.get(
                                        key
                                    )
                                ).strip()
                            )

                            break

                elif item:

                    values.append(
                        str(
                            item
                        ).strip()
                    )


        elif isinstance(
            parsed,
            dict
        ):

            for key in [
                "name",
                "language"
            ]:

                if parsed.get(
                    key
                ):

                    values.append(
                        str(
                            parsed.get(
                                key
                            )
                        ).strip()
                    )

                    break


        if values:

            return ", ".join(
                dict.fromkeys(
                    values
                )
            )


    except Exception:

        pass


    text = re.sub(
        r"[\[\]\{\}'\"]",
        " ",
        text
    )

    text = re.sub(
        r"\bid\s*:\s*\d+",
        " ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bname\s*:",
        " ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )


    return text.strip()


# =========================================================
# MOVIE INFORMATION
# =========================================================

def get_movie_info(index):

    info = {}


    # -----------------------------------------------------
    # GENRE
    # -----------------------------------------------------

    if "genres" in movies.columns:

        value = movies.loc[
            index,
            "genres"
        ]

        info["genre"] = clean_genre(
            value
        )

    elif genre_column is not None:

        info["genre"] = clean_genre(
            movies.loc[
                index,
                genre_column
            ]
        )

    else:

        info["genre"] = "Not Available"


    # -----------------------------------------------------
    # RATING
    # -----------------------------------------------------

    if "rating" in movies.columns:

        value = movies.loc[
            index,
            "rating"
        ]

    elif rating_column is not None:

        value = movies.loc[
            index,
            rating_column
        ]

    else:

        value = None


    try:

        if pd.notna(
            value
        ):

            info["rating"] = (
                f"{float(value):.1f}"
            )

        else:

            info["rating"] = (
                "Not Available"
            )

    except Exception:

        info["rating"] = str(
            value
        )


    # -----------------------------------------------------
    # YEAR
    # -----------------------------------------------------

    if "year" in movies.columns:

        value = movies.loc[
            index,
            "year"
        ]

    elif year_column is not None:

        value = movies.loc[
            index,
            year_column
        ]

    else:

        value = None


    if pd.notna(
        value
    ):

        try:

            numeric_year = float(
                value
            )

            if numeric_year > 0:

                info["year"] = str(
                    int(numeric_year)
                )

            else:

                info["year"] = (
                    "Not Available"
                )

        except Exception:

            match = re.search(
                r"(19|20)\d{2}",
                str(value)
            )

            if match:

                info["year"] = (
                    match.group()
                )

            else:

                info["year"] = str(
                    value
                )

    else:

        info["year"] = (
            "Not Available"
        )


    # -----------------------------------------------------
    # LANGUAGE
    # -----------------------------------------------------

    language_value = ""


    # Training.py saves these prepared columns.
    # Prefer languages first because this is the actual
    # language information used for display.

    if "languages" in movies.columns:

        language_value = movies.loc[
            index,
            "languages"
        ]

    elif "primary_language" in movies.columns:

        language_value = movies.loc[
            index,
            "primary_language"
        ]

    elif language_cinema_column is not None:

        language_value = movies.loc[
            index,
            language_cinema_column
        ]

    elif languages_column is not None:

        language_value = movies.loc[
            index,
            languages_column
        ]


    if pd.notna(
        language_value
    ):

        cleaned = clean_language(
            language_value
        )

        info["language"] = (
            cleaned
            if cleaned
            else "Not Available"
        )

    else:

        info["language"] = (
            "Not Available"
        )


    return info


# =========================================================
# FAVORITES
# =========================================================

def load_favorites():

    if not os.path.exists(
        FAVORITES_FILE
    ):

        return []


    try:

        with open(
            FAVORITES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        if isinstance(
            data,
            list
        ):

            return data


    except Exception:

        pass


    return []


# =========================================================
# SAVE FAVORITES
# =========================================================

def save_favorites(
    favorites
):

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


        return True


    except Exception as error:

        messagebox.showerror(
            "Favorite Error",
            str(error)
        )

        return False


# =========================================================
# ADD FAVORITE
# =========================================================

def add_to_favorites(
    movie_data
):

    favorites = load_favorites()


    title = str(
        movie_data.get(
            "title",
            ""
        )
    ).strip()


    for movie in favorites:

        if isinstance(
            movie,
            dict
        ):

            old_title = str(
                movie.get(
                    "title",
                    ""
                )
            ).strip()


            if (
                old_title.lower()
                == title.lower()
            ):

                messagebox.showinfo(
                    "Already Added",
                    "This movie is already in My Favorites."
                )

                return


    favorites.append(
        movie_data
    )


    if save_favorites(
        favorites
    ):

        messagebox.showinfo(
            "Added",
            title
            + " added to My Favorites."
        )


# =========================================================
# OPEN OTHER PAGE
# =========================================================

def open_page(
    file_name
):

    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )


    if not os.path.exists(
        file_path
    ):

        messagebox.showerror(
            "Page Not Found",
            file_name
            + " was not found."
        )

        return


    root.destroy()


    import subprocess
    import sys


    subprocess.Popen([
        sys.executable,
        file_path
    ])


# =========================================================
# LOGOUT
# =========================================================

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


    if os.path.exists(
        login_file
    ):

        import subprocess
        import sys


        subprocess.Popen([
            sys.executable,
            login_file
        ])


# =========================================================
# FILTER MOVIES
# =========================================================

def get_filtered_movies():

    filtered = movies.copy()


    selected_language = (
        language_var.get()
    )


    selected_genre = (
        genre_var.get()
    )


    # -----------------------------------------------------
    # LANGUAGE
    # -----------------------------------------------------

    if (
        selected_language
        != "All Languages"
    ):

        language_columns = []


        if "language_cinema" in filtered.columns:

            language_columns.append(
                "language_cinema"
            )


        if "languages" in filtered.columns:

            language_columns.append(
                "languages"
            )


        if "primary_language" in filtered.columns:

            language_columns.append(
                "primary_language"
            )


        if language_columns:

            mask = pd.Series(
                False,
                index=filtered.index
            )


            for column in language_columns:

                mask = (
                    mask
                    |
                    filtered[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        selected_language.lower(),
                        na=False
                    )
                )


            filtered = filtered[
                mask
            ]


    # -----------------------------------------------------
    # GENRE
    # -----------------------------------------------------

    if (
        selected_genre
        != "All Genres"
    ):

        if "genres" in filtered.columns:

            filtered = filtered[
                filtered[
                    "genres"
                ].apply(
                    lambda value:
                    selected_genre.lower()
                    in [
                        x.strip().lower()
                        for x in clean_genre(
                            value
                        ).split(",")
                    ]
                )
            ]

        elif genre_column is not None:

            filtered = filtered[
                filtered[
                    genre_column
                ].apply(
                    lambda value:
                    selected_genre.lower()
                    in [
                        x.strip().lower()
                        for x in clean_genre(
                            value
                        ).split(",")
                    ]
                )
            ]


    return filtered


# =========================================================
# GET FEATURE VECTOR
# =========================================================
# IMPORTANT:
# Training.py trains KNN using exactly these 7 features.
#
# year
# rating
# genre_count
# language_count
# genre_encoded
# language_encoded
# language_cinema_encoded
#
# Therefore Recommendation.py MUST create the same
# 7-feature vector and use the SAME scaler.
# =========================================================

def get_feature_vector(
    index
):

    try:

        feature_values = []

        for feature in required_features:

            value = movies.loc[
                index,
                feature
            ]

            try:

                numeric_value = float(
                    value
                )

            except Exception:

                numeric_value = 0.0


            if not np.isfinite(
                numeric_value
            ):

                numeric_value = 0.0


            feature_values.append(
                numeric_value
            )


        vector = np.asarray(
            feature_values,
            dtype=np.float64
        ).reshape(
            1,
            -1
        )


        # -------------------------------------------------
        # SAME SCALER USED BY TRAINING.PY
        # -------------------------------------------------

        scaled_vector = (
            knn_scaler.transform(
                vector
            )
        )


        scaled_vector = np.asarray(
            scaled_vector,
            dtype=np.float64
        )


        if scaled_vector.shape != (
            1,
            len(required_features)
        ):

            raise ValueError(
                "Feature shape mismatch. "
                "Expected "
                + str(
                    len(required_features)
                )
                + " features but received "
                + str(
                    scaled_vector.shape
                )
            )


        return scaled_vector


    except Exception as error:

        raise ValueError(
            "Unable to create trained movie "
            "feature vector.\n\n"
            + str(error)
        )


# =========================================================
# RECOMMENDATION
# =========================================================

def recommend_movies():

    movie_name = (
        movie_entry
        .get()
        .strip()
    )


    if not movie_name:

        messagebox.showwarning(
            "Movie Required",
            "Please enter a movie name."
        )

        return


    # =====================================================
    # FIND MOVIE IN COMPLETE DATASET
    # =====================================================

    all_titles = (
        movies[
            title_column
        ]
        .astype(str)
        .str.strip()
    )


    search_text = (
        movie_name
        .lower()
        .strip()
    )


    # -----------------------------------------------------
    # EXACT MATCH FIRST
    # -----------------------------------------------------

    exact_matches = movies[
        all_titles.str.lower()
        == search_text
    ]


    # -----------------------------------------------------
    # PARTIAL MATCH SECOND
    # -----------------------------------------------------

    if exact_matches.empty:

        matches = movies[
            all_titles
            .str.lower()
            .str.contains(
                re.escape(
                    search_text
                ),
                na=False
            )
        ]

    else:

        matches = exact_matches


    # -----------------------------------------------------
    # NO MOVIE
    # -----------------------------------------------------

    if matches.empty:

        messagebox.showerror(
            "Movie Not Found",
            "No movie found for:\n\n"
            + movie_name
        )

        return


    # -----------------------------------------------------
    # SELECT FIRST MATCH
    # -----------------------------------------------------

    selected_index = (
        matches.index[0]
    )


    selected_title = str(
        movies.loc[
            selected_index,
            title_column
        ]
    )


    # =====================================================
    # GET SELECTED MOVIE VECTOR
    # =====================================================

    try:

        feature_vector = (
            get_feature_vector(
                selected_index
            )
        )


    except Exception as error:

        messagebox.showerror(
            "Feature Error",
            "Unable to create movie features.\n\n"
            + str(error)
            + "\n\n"
            "Please run Training.py again."
        )

        return


    # =====================================================
    # KNN SHAPE CHECK
    # =====================================================

    try:

        expected_features = (
            len(required_features)
        )


        if feature_vector.shape != (
            1,
            expected_features
        ):

            feature_vector = (
                np.asarray(
                    feature_vector,
                    dtype=np.float64
                )
                .reshape(
                    1,
                    expected_features
                )
            )


    except Exception as error:

        messagebox.showerror(
            "Feature Error",
            "Invalid feature shape.\n\n"
            + str(error)
        )

        return


    # =====================================================
    # KNN
    # =====================================================

    try:

        total_movies = len(
            movies
        )


        number = min(
            11,
            total_movies
        )


        if number <= 0:

            raise ValueError(
                "No movies available in the model."
            )


        distances, indices = (
            knn_model.kneighbors(
                feature_vector,
                n_neighbors=number
            )
        )


    except Exception as error:

        messagebox.showerror(
            "Recommendation Error",
            "Unable to generate recommendations.\n\n"
            + str(error)
            + "\n\n"
            "Please run Training.py again "
            "and then start Recommendation.py."
        )

        return


    # =====================================================
    # CLEAR RESULTS
    # =====================================================

    for widget in (
        result_inner
        .winfo_children()
    ):

        widget.destroy()


    # =====================================================
    # SELECTED MOVIE
    # =====================================================

    selected_info = (
        get_movie_info(
            selected_index
        )
    )


    selected_card = tk.Frame(
        result_inner,
        bg=ENTRY_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )


    selected_card.pack(
        fill="x",
        padx=18,
        pady=(18, 10)
    )


    tk.Label(
        selected_card,
        text="SELECTED MOVIE",
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=ENTRY_COLOR,
        fg=PURPLE
    ).pack(
        anchor="w",
        padx=18,
        pady=(12, 2)
    )


    tk.Label(
        selected_card,
        text=selected_title,
        font=(
            "Segoe UI",
            17,
            "bold"
        ),
        bg=ENTRY_COLOR,
        fg=TEXT_COLOR,
        wraplength=900,
        justify="left"
    ).pack(
        anchor="w",
        padx=18
    )


    selected_details = []


    if (
        selected_info["genre"]
        != "Not Available"
    ):

        selected_details.append(
            "🎭 "
            + selected_info["genre"]
        )


    if (
        selected_info["rating"]
        != "Not Available"
    ):

        selected_details.append(
            "⭐ "
            + selected_info["rating"]
        )


    if (
        selected_info["year"]
        != "Not Available"
    ):

        selected_details.append(
            "📅 "
            + selected_info["year"]
        )


    tk.Label(
        selected_card,
        text="    ".join(
            selected_details
        ),
        font=(
            "Segoe UI",
            9,
            "bold"
        ),
        bg=ENTRY_COLOR,
        fg=SECONDARY_TEXT,
        wraplength=900,
        justify="left"
    ).pack(
        anchor="w",
        padx=18,
        pady=(5, 12)
    )


    # =====================================================
    # HEADING
    # =====================================================

    tk.Label(
        result_inner,
        text="SIMILAR MOVIES",
        font=(
            "Segoe UI",
            15,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=DARK_PURPLE
    ).pack(
        anchor="w",
        padx=18,
        pady=(8, 5)
    )


    # =====================================================
    # RECOMMENDED MOVIES
    # =====================================================

    count = 0

    already_added = set()


    for position in range(
        1,
        len(indices[0])
    ):

        # -------------------------------------------------
        # KNN index -> prepared DataFrame position
        # -------------------------------------------------

        model_index = int(
            indices[0][position]
        )


        if (
            model_index < 0
            or model_index >= len(movies)
        ):

            continue


        # IMPORTANT:
        # KNN was fitted using DataFrame row order.
        # Therefore use iloc, not movies.index[model_index].
        data_index = movies.index[
            model_index
        ]


        recommended_title = str(
            movies.loc[
                data_index,
                title_column
            ]
        )


        # -------------------------------------------------
        # DUPLICATES
        # -------------------------------------------------

        title_key = (
            recommended_title
            .strip()
            .lower()
        )


        if title_key in already_added:

            continue


        already_added.add(
            title_key
        )


        # -------------------------------------------------
        # DON'T SHOW SELECTED
        # -------------------------------------------------

        if (
            title_key
            == selected_title
            .strip()
            .lower()
        ):

            continue


        # -------------------------------------------------
        # APPLY LANGUAGE FILTER
        # -------------------------------------------------

        selected_language = (
            language_var.get()
        )

        selected_genre = (
            genre_var.get()
        )


        if (
            selected_language
            != "All Languages"
        ):

            info_language = (
                get_movie_info(
                    data_index
                )["language"]
            )


            if (
                selected_language.lower()
                not in info_language.lower()
            ):

                continue


        # -------------------------------------------------
        # APPLY GENRE FILTER
        # -------------------------------------------------

        if (
            selected_genre
            != "All Genres"
        ):

            info_genre = (
                get_movie_info(
                    data_index
                )["genre"]
            )


            genre_values = [
                x.strip().lower()
                for x in info_genre.split(",")
            ]


            if (
                selected_genre.lower()
                not in genre_values
            ):

                continue


        info = get_movie_info(
            data_index
        )


        # -------------------------------------------------
        # DISTANCE
        # -------------------------------------------------

        distance = float(
            distances[
                0
            ][
                position
            ]
        )


        # -------------------------------------------------
        # SIMILARITY
        # -----------------------------------------------------

        similarity = (
            1.0
            /
            (
                1.0
                + max(
                    0.0,
                    distance
                )
            )
        ) * 100.0


        similarity = max(
            0,
            min(
                100,
                similarity
            )
        )


        # =================================================
        # MOVIE CARD
        # =================================================

        movie_card = tk.Frame(
            result_inner,
            bg=CARD_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )


        movie_card.pack(
            fill="x",
            padx=18,
            pady=6
        )


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        tk.Label(
            movie_card,
            text=(
                f"{count + 1:02d}   "
                f"{recommended_title}"
            ),
            font=(
                "Segoe UI",
                12,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            anchor="w",
            wraplength=600,
            justify="left"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12, 3)
        )


        # -------------------------------------------------
        # SIMILARITY
        # -------------------------------------------------

        tk.Label(
            movie_card,
            text=(
                f"{similarity:.1f}% similar"
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=PURPLE
        ).grid(
            row=0,
            column=1,
            sticky="e",
            padx=15,
            pady=(12, 3)
        )


        # -------------------------------------------------
        # DETAILS
        # -------------------------------------------------

        details = []


        if (
            info["genre"]
            != "Not Available"
        ):

            details.append(
                "🎭 "
                + info["genre"]
            )


        if (
            info["rating"]
            != "Not Available"
        ):

            details.append(
                "⭐ "
                + info["rating"]
            )


        if (
            info["year"]
            != "Not Available"
        ):

            details.append(
                "📅 "
                + info["year"]
            )


        tk.Label(
            movie_card,
            text="    ".join(
                details
            ),
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT,
            wraplength=850,
            justify="left"
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=15,
            pady=(0, 8)
        )


        # -------------------------------------------------
        # FAVORITE
        # -------------------------------------------------

        favorite_data = {
            "title":
                recommended_title,

            "genre":
                info["genre"],

            "rating":
                info["rating"],

            "year":
                info["year"],

            "language":
                info["language"]
        }


        tk.Button(
            movie_card,
            text="❤️ ADD TO FAVORITES",
            font=(
                "Segoe UI",
                8,
                "bold"
            ),
            bg=BUTTON_COLOR,
            fg=WHITE,
            activebackground=DARK_PURPLE,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda data=favorite_data:
                add_to_favorites(data)
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=15,
            pady=10,
            ipadx=8,
            ipady=6
        )


        movie_card.grid_columnconfigure(
            0,
            weight=1
        )


        count += 1


        if count >= 10:

            break


    # =====================================================
    # NO FILTERED RECOMMENDATIONS
    # =====================================================

    if count == 0:

        tk.Label(
            result_inner,
            text=(
                "No similar movies found "
                "for the selected filters."
            ),
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=MUTED_TEXT
        ).pack(
            pady=30
        )


    # =====================================================
    # UPDATE SCROLL
    # =====================================================

    result_inner.update_idletasks()


    result_canvas.configure(
        scrollregion=result_canvas.bbox(
            "all"
        )
    )


    result_canvas.yview_moveto(
        0
    )


# =========================================================
# RANDOM MOVIE
# =========================================================

def random_movie():

    filtered = (
        get_filtered_movies()
    )


    if filtered.empty:

        messagebox.showwarning(
            "No Movies",
            "No movies found."
        )

        return


    selected_index = (
        filtered
        .sample(1)
        .index[0]
    )


    movie_entry.delete(
        0,
        tk.END
    )


    movie_entry.insert(
        0,
        str(
            movies.loc[
                selected_index,
                title_column
            ]
        )
    )


    recommend_movies()


# =========================================================
# RESET
# =========================================================

def reset():

    movie_entry.delete(
        0,
        tk.END
    )


    language_var.set(
        "All Languages"
    )


    genre_var.set(
        "All Genres"
    )


    for widget in (
        result_inner
        .winfo_children()
    ):

        widget.destroy()


    tk.Label(
        result_inner,
        text=(
            "\n\n\n"
            "SELECT A MOVIE TO GET\n"
            "PERSONALIZED RECOMMENDATIONS"
        ),
        font=(
            "Segoe UI",
            13,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=MUTED_TEXT,
        justify="center"
    ).pack(
        expand=True
    )


    result_canvas.configure(
        scrollregion=result_canvas.bbox(
            "all"
        )
    )


    result_canvas.yview_moveto(
        0
    )


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Movie Recommendation System"
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

main_container = tk.Frame(
    root,
    bg=BG_COLOR
)

main_container.pack(
    fill="both",
    expand=True
)


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    main_container,
    bg=SIDEBAR_COLOR,
    width=280
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
    font=(
        "Segoe UI",
        23,
        "bold"
    ),
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(45, 0)
)


tk.Label(
    sidebar,
    text="RECOMMENDATION",
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    bg=SIDEBAR_COLOR,
    fg=LIGHT_PURPLE
).pack()


tk.Label(
    sidebar,
    text="SYSTEM",
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    bg=SIDEBAR_COLOR,
    fg=WHITE
).pack(
    pady=(0, 30)
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
    pady=(22, 8)
)


def sidebar_button(
    text,
    command,
    active=False
):

    color = (
        PURPLE
        if active
        else BUTTON_COLOR
    )


    button = tk.Button(
        sidebar,
        text=text,
        font=(
            "Segoe UI",
            10,
            "bold"
        ),
        bg=color,
        fg=WHITE,
        activebackground=color,
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
        pady=5,
        ipady=10
    )


sidebar_button(
    "HOME",
    lambda:
    open_page("home.py")
)


sidebar_button(
    "MOVIE RECOMMENDATION",
    lambda: None,
    active=True
)


sidebar_button(
    "MY FAVORITES ",
    lambda:
    open_page("favorite.py")
)


sidebar_button(
    "MY PROFILE",
    lambda:
    open_page("profile.py")
)





bottom = tk.Frame(
    sidebar,
    bg=SIDEBAR_COLOR
)

bottom.pack(
    side="bottom",
    fill="x",
    pady=25
)


tk.Button(
    bottom,
    text="LOGOUT",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
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
    text="MOVIE RECOMMENDATION",
    font=(
        "Segoe UI",
        19,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left",
    padx=40
)


tk.Label(
    header,
    text="●  RECOMMENDATION ENGINE READY",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
).pack(
    side="right",
    padx=40
)



content = tk.Frame(
    right_area,
    bg=BG_COLOR
)

content.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=22
)


tk.Label(
    content,
    text="Find Your Next Movie",
    font=(
        "Segoe UI",
        27,
        "bold"
    ),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    pady=(0, 4)
)


tk.Label(
    content,
    text=(
        "Choose a genre or language and "
        "find similar movies."
    ),
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
).pack(
    pady=(0, 15)
)



search_card = tk.Frame(
    content,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

search_card.pack(
    fill="x",
    padx=20
)


tk.Frame(
    search_card,
    bg=PURPLE,
    height=4
).pack(
    fill="x"
)


search_content = tk.Frame(
    search_card,
    bg=CARD_COLOR
)

search_content.pack(
    pady=17
)



tk.Label(
    search_content,
    text="LANGUAGE",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=0,
    padx=6
)


languages = [
    "All Languages",
    "English",
    "Hindi",
    "Marathi",
    "Telugu",
    "Tamil",
    "Korean",
    "Japanese"
]


language_var = tk.StringVar(
    value="All Languages"
)


language_menu = tk.OptionMenu(
    search_content,
    language_var,
    *languages
)


language_menu.config(
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=ENTRY_COLOR,
    fg=TEXT_COLOR,
    activebackground=LIGHT_PURPLE,
    activeforeground=WHITE,
    width=13,
    relief="flat",
    bd=0
)


language_menu.grid(
    row=0,
    column=1,
    padx=8
)


genre_list = [
    "All Genres"
]


if "genres" in movies.columns:

    all_genres = set()


    for value in movies[
        "genres"
    ].dropna():

        cleaned = clean_genre(
            value
        )


        for genre in (
            cleaned.split(",")
        ):

            genre = genre.strip()


            if (
                genre
                and genre
                != "Not Available"
            ):

                all_genres.add(
                    genre
                )


    genre_list.extend(
        sorted(
            all_genres
        )
    )

elif genre_column is not None:

    all_genres = set()


    for value in movies[
        genre_column
    ].dropna():

        cleaned = clean_genre(
            value
        )


        for genre in (
            cleaned.split(",")
        ):

            genre = genre.strip()


            if (
                genre
                and genre
                != "Not Available"
            ):

                all_genres.add(
                    genre
                )


    genre_list.extend(
        sorted(
            all_genres
        )
    )



tk.Label(
    search_content,
    text="GENRE",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=2,
    padx=6
)


genre_var = tk.StringVar(
    value="All Genres"
)


genre_menu = tk.OptionMenu(
    search_content,
    genre_var,
    *genre_list
)


genre_menu.config(
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=ENTRY_COLOR,
    fg=TEXT_COLOR,
    activebackground=LIGHT_PURPLE,
    activeforeground=WHITE,
    width=13,
    relief="flat",
    bd=0
)


genre_menu.grid(
    row=0,
    column=3,
    padx=8
)



tk.Label(
    search_content,
    text="MOVIE",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
).grid(
    row=0,
    column=4,
    padx=6
)


entry_frame = tk.Frame(
    search_content,
    bg=ENTRY_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)


entry_frame.grid(
    row=0,
    column=5,
    padx=8
)


movie_entry = tk.Entry(
    entry_frame,
    font=(
        "Segoe UI",
        11,
        "bold"
    ),
    width=22,
    bg=ENTRY_COLOR,
    fg=BLACK,
    insertbackground=PURPLE,
    relief="flat",
    bd=0
)


movie_entry.pack(
    padx=10,
    pady=8,
    ipady=3
)



tk.Button(
    search_content,
    text="RECOMMEND",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_COLOR,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=recommend_movies
).grid(
    row=0,
    column=6,
    padx=5,
    ipadx=10,
    ipady=8
)


# =========================================================
# RANDOM BUTTON
# =========================================================

tk.Button(
    search_content,
    text="RANDOM",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=PURPLE,
    fg=WHITE,
    activebackground=DARK_PURPLE,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=random_movie
).grid(
    row=0,
    column=7,
    padx=5,
    ipadx=8,
    ipady=8
)


# =========================================================
# RESULT HEADER
# =========================================================

result_header = tk.Frame(
    content,
    bg=BG_COLOR
)

result_header.pack(
    fill="x",
    padx=20,
    pady=(15, 6)
)


tk.Label(
    result_header,
    text="RECOMMENDED MOVIES",
    font=(
        "Segoe UI",
        16,
        "bold"
    ),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(
    side="left"
)


tk.Button(
    result_header,
    text="↻ RESET",
    font=(
        "Segoe UI",
        9,
        "bold"
    ),
    bg=BUTTON_COLOR,
    fg=WHITE,
    activebackground=BUTTON_COLOR,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    cursor="hand2",
    command=reset
).pack(
    side="right",
    ipadx=12,
    ipady=5
)


# =========================================================
# RESULT FRAME
# =========================================================

result_frame = tk.Frame(
    content,
    bg=PURPLE,
    padx=2,
    pady=2
)

result_frame.pack(
    fill="both",
    expand=True,
    padx=20
)


result_canvas = tk.Canvas(
    result_frame,
    bg=CARD_COLOR,
    highlightthickness=0
)

result_canvas.pack(
    side="left",
    fill="both",
    expand=True
)


scrollbar = tk.Scrollbar(
    result_frame,
    orient="vertical",
    command=result_canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)


result_canvas.configure(
    yscrollcommand=scrollbar.set
)


result_inner = tk.Frame(
    result_canvas,
    bg=CARD_COLOR
)


canvas_window = (
    result_canvas.create_window(
        (0, 0),
        window=result_inner,
        anchor="nw"
    )
)


def update_scroll(
    event=None
):

    result_canvas.configure(
        scrollregion=
        result_canvas.bbox("all")
    )


def resize_inner(
    event
):

    result_canvas.itemconfig(
        canvas_window,
        width=event.width
    )


result_inner.bind(
    "<Configure>",
    update_scroll
)

result_canvas.bind(
    "<Configure>",
    resize_inner
)



def mouse_wheel(
    event
):

    if event.delta:

        result_canvas.yview_scroll(
            int(
                -1
                * (
                    event.delta
                    / 120
                )
            ),
            "units"
        )


result_canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)



tk.Label(
    result_inner,
    text=(
        "\n\n\n"
        "SELECT A MOVIE TO GET\n"
        "PERSONALIZED RECOMMENDATIONS"
    ),
    font=(
        "Segoe UI",
        13,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=MUTED_TEXT,
    justify="center"
).pack(
    expand=True
)



root.bind(
    "<Return>",
    lambda event:
    recommend_movies()
)


movie_entry.focus()

root.mainloop()