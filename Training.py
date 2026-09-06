import os
import re
import ast
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.join(BASE_DIR, "Dataset", "Movies (1970-2023).csv")
MODEL_DIR = os.path.join(BASE_DIR, "Model")
os.makedirs(MODEL_DIR, exist_ok=True)

KNN_FILE = os.path.join(MODEL_DIR, "knn_model.pkl")
MOVIES_FILE = os.path.join(MODEL_DIR, "movies.pkl")
SCALER_FILE = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODERS_FILE = os.path.join(MODEL_DIR, "encoders.pkl")
ANN_FILE = os.path.join(MODEL_DIR, "movie_ann_model.keras")
ANN_SCALER_FILE = os.path.join(MODEL_DIR, "ann_scaler.pkl")

try:
    movies = pd.read_csv(DATASET_FILE, low_memory=False)
except Exception as error:
    print("\nERROR while reading dataset:")
    print(error)
    raise SystemExit

print("\nDataset loaded successfully.")
print("Total movies:", len(movies))
print("Total columns:", len(movies.columns))

if len(movies) < 2:
    print("\nERROR: Dataset contains fewer than 2 movies.")
    raise SystemExit

movies.columns = movies.columns.astype(str).str.strip()

def find_column(names):
    column_map = {str(column).lower().strip(): column for column in movies.columns}
    for name in names:
        key = str(name).lower().strip()
        if key in column_map:
            return column_map[key]
    return None

title_column = find_column(["title", "movie title", "movie_title", "name"])
genre_column = find_column(["genres", "genre"])
language_cinema_column = find_column(["language cinema", "language_cinema", "cinema"])
languages_column = find_column(["languages", "language", "original_language"])
year_column = find_column(["year", "release_year", "release year", "release_date"])
rating_column = find_column(["rating", "ratings", "vote_average", "imdb_rating"])
votes_column = find_column(["vote_count", "votes", "rating_count"])

print("\nDetected columns:")
print("Title           :", title_column)
print("Genres          :", genre_column)
print("Language Cinema :", language_cinema_column)
print("Languages       :", languages_column)
print("Year            :", year_column)
print("Rating          :", rating_column)
print("Votes           :", votes_column)

if title_column is None:
    print("\nERROR: Movie title column not found.")
    print("\nAvailable columns:")
    print(list(movies.columns))
    raise SystemExit

def parse_tmdb_list(value):
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, list):
            result = []
            for item in parsed:
                if isinstance(item, dict):
                    name = item.get("name")
                    if name:
                        result.append(str(name).strip())
                elif isinstance(item, str):
                    item = item.strip()
                    if item:
                        result.append(item)
            return result
        if isinstance(parsed, dict):
            name = parsed.get("name")
            if name:
                return [str(name).strip()]
    except Exception:
        pass

    matches = re.findall(r"""['"]name['"]\s*:\s*['"]([^'"]+)['"]""", text)
    if matches:
        return [item.strip() for item in matches if item.strip()]

    cleaned = re.sub(r"[\[\]\{\}'\"]", "", text)
    cleaned = re.sub(r"\bid\s*:\s*\d+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bname\s*:", "", cleaned, flags=re.IGNORECASE)
    parts = re.split(r"[,|;/]+", cleaned)

    return [item.strip() for item in parts if item.strip()]

def clean_genres(value):
    genres = parse_tmdb_list(value)
    result = []
    seen = set()

    for genre in genres:
        genre = str(genre).strip()
        if not genre:
            continue
        genre = re.sub(r"\bid\s*:\s*\d+", "", genre, flags=re.IGNORECASE)
        genre = re.sub(r"\bname\s*:", "", genre, flags=re.IGNORECASE)
        genre = genre.strip("[]{}'\" ")
        genre = re.sub(r"\s+", " ", genre)
        if not genre:
            continue
        key = genre.lower()
        if key not in seen:
            seen.add(key)
            result.append(genre.lower())

    return ", ".join(result)

def clean_text(value):
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if not text:
        return ""

    try:
        parsed = ast.literal_eval(text)
        values = []

        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    for key in ["name", "title", "language"]:
                        if item.get(key):
                            values.append(str(item[key]))
                            break
                elif item:
                    values.append(str(item))

        elif isinstance(parsed, dict):
            for key in ["name", "title", "language"]:
                if parsed.get(key):
                    values.append(str(parsed[key]))
                    break

        if values:
            return " ".join(values).lower()

    except Exception:
        pass

    text = re.sub(r"[\[\]\{\}'\"]", " ", text)
    text = re.sub(r"\bid\s*:\s*\d+", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bname\s*:", " ", text, flags=re.IGNORECASE)
    text = text.replace("|", " ").replace(",", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()

def extract_year(value):
    if pd.isna(value):
        return 0.0

    match = re.search(r"(19|20)\d{2}", str(value))

    if match:
        try:
            return float(match.group())
        except Exception:
            return 0.0

    return 0.0

def safe_number(value):
    if pd.isna(value):
        return 0.0

    try:
        number = float(value)
        if np.isfinite(number):
            return number
    except Exception:
        pass

    return 0.0

prepared = pd.DataFrame()

prepared["title"] = (
    movies[title_column]
    .fillna("")
    .astype(str)
    .str.strip()
)

if genre_column is not None:
    prepared["genres"] = movies[genre_column].apply(clean_genres)
else:
    prepared["genres"] = ""

if language_cinema_column is not None:
    prepared["language_cinema"] = movies[language_cinema_column].apply(clean_text)
else:
    prepared["language_cinema"] = ""

if languages_column is not None:
    prepared["languages"] = movies[languages_column].apply(clean_text)
else:
    prepared["languages"] = ""

if year_column is not None:
    prepared["year"] = movies[year_column].apply(extract_year)
else:
    prepared["year"] = 0.0

if rating_column is not None:
    prepared["rating"] = movies[rating_column].apply(safe_number)
else:
    prepared["rating"] = 0.0

if votes_column is not None:
    prepared["vote_count"] = movies[votes_column].apply(safe_number)
else:
    prepared["vote_count"] = 0.0

prepared = prepared[prepared["title"].str.strip() != ""].copy()

old_count = len(prepared)
prepared = prepared.drop_duplicates(subset=["title"], keep="first")
new_count = len(prepared)

print("\nDuplicate movies removed:", old_count - new_count)

prepared = prepared.reset_index(drop=True)

if len(prepared) < 2:
    print("\nERROR: Not enough movies after cleaning.")
    raise SystemExit

print("Movies available for training:", len(prepared))

prepared["year"] = pd.to_numeric(
    prepared["year"], errors="coerce"
).fillna(0).clip(1900, 2030)

prepared["rating"] = pd.to_numeric(
    prepared["rating"], errors="coerce"
).fillna(0).clip(0, 10)

prepared["vote_count"] = pd.to_numeric(
    prepared["vote_count"], errors="coerce"
).fillna(0).clip(lower=0)

def get_genre_count(text):
    if not text:
        return 0
    parts = [x.strip() for x in str(text).split(",") if x.strip()]
    return len(parts)

prepared["genre_count"] = prepared["genres"].apply(get_genre_count)

def get_language_count(text):
    if not text:
        return 0
    parts = re.split(r"[,|;/]+", str(text))
    parts = [x.strip() for x in parts if x.strip()]
    return len(parts)

prepared["language_count"] = prepared["languages"].apply(get_language_count)

def get_primary_genre(text):
    if not text:
        return "unknown"
    parts = [x.strip() for x in str(text).split(",") if x.strip()]
    return parts[0] if parts else "unknown"

prepared["primary_genre"] = prepared["genres"].apply(get_primary_genre)

def get_primary_language(text):
    if not text:
        return "unknown"
    parts = re.split(r"[,|;/]+", str(text))
    parts = [x.strip() for x in parts if x.strip()]
    return parts[0] if parts else "unknown"

prepared["primary_language"] = prepared["languages"].apply(get_primary_language)

genre_encoder = LabelEncoder()
language_encoder = LabelEncoder()
cinema_encoder = LabelEncoder()

prepared["genre_encoded"] = genre_encoder.fit_transform(prepared["primary_genre"])
prepared["language_encoded"] = language_encoder.fit_transform(prepared["primary_language"])

prepared["language_cinema_encoded"] = cinema_encoder.fit_transform(
    prepared["language_cinema"].replace("", "unknown").astype(str)
)

encoders = {
    "genre": genre_encoder,
    "language": language_encoder,
    "language_cinema": cinema_encoder
}

with open(ENCODERS_FILE, "wb") as file:
    pickle.dump(encoders, file)

knn_features = [
    "year",
    "rating",
    "genre_count",
    "language_count",
    "genre_encoded",
    "language_encoded",
    "language_cinema_encoded"
]

print("\nKNN Features:")
for feature in knn_features:
    print(" -", feature)

X_knn = prepared[knn_features].copy()
X_knn = X_knn.replace([np.inf, -np.inf], np.nan)
X_knn = X_knn.fillna(0)
X_knn = np.asarray(X_knn, dtype=np.float64)

if X_knn.ndim != 2:
    raise ValueError("KNN feature matrix must be 2D.")

if X_knn.shape[1] != 7:
    raise ValueError(
        "KNN requires exactly 7 features. "
        f"Found {X_knn.shape[1]}."
    )

print("\nOriginal KNN feature shape:", X_knn.shape)

knn_scaler = StandardScaler()
X_knn_scaled = knn_scaler.fit_transform(X_knn)
X_knn_scaled = np.asarray(X_knn_scaled, dtype=np.float64)

print("Scaled KNN feature shape:", X_knn_scaled.shape)

n_neighbors = min(11, len(prepared))

knn_model = NearestNeighbors(
    n_neighbors=n_neighbors,
    metric="cosine",
    algorithm="brute"
)

knn_model.fit(X_knn_scaled)

print("\nKNN training completed.")

with open(SCALER_FILE, "wb") as file:
    pickle.dump(knn_scaler, file)

prepared["features"] = [vector.tolist() for vector in X_knn_scaled]
prepared["knn_index"] = np.arange(len(prepared))

with open(KNN_FILE, "wb") as file:
    pickle.dump(knn_model, file)

print("KNN model saved.")

ann_features = [
    "year",
    "genre_count",
    "language_count",
    "genre_encoded",
    "language_encoded",
    "language_cinema_encoded"
]

X_ann = prepared[ann_features].copy()

median_rating = prepared["rating"].median()

if not np.isfinite(median_rating):
    median_rating = 5.0

if median_rating <= 0:
    median_rating = 5.0

y = (prepared["rating"] >= median_rating).astype(np.int32)

print("\nMedian rating:", round(float(median_rating), 2))
print("\nClass distribution:")
print(y.value_counts())

class_counts = y.value_counts()

if len(class_counts) < 2:
    print("\nERROR: ANN target contains only one class.")
    raise SystemExit

if class_counts.min() < 2:
    print("\nERROR: Not enough samples in one class.")
    raise SystemExit

X_ann = X_ann.replace([np.inf, -np.inf], np.nan)
X_ann = X_ann.fillna(0)
X_ann = np.asarray(X_ann, dtype=np.float64)

ann_scaler = StandardScaler()
X_ann_scaled = ann_scaler.fit_transform(X_ann)

X_train, X_test, y_train, y_test = train_test_split(
    X_ann_scaled,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
print("ANN input features:", X_train.shape[1])

ann_model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation="relu", kernel_regularizer=l2(0.0005)),
    Dropout(0.25),
    Dense(32, activation="relu", kernel_regularizer=l2(0.0005)),
    Dropout(0.15),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])

ann_model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=8,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=4,
    min_lr=0.00001,
    verbose=1
)

ann_model.summary()

history = ann_model.fit(
    X_train,
    y_train,
    validation_split=0.20,
    epochs=40,
    batch_size=64,
    callbacks=[early_stop, reduce_lr],
    verbose=1
)

actual_epochs = len(history.history["loss"])
print("\nActual epochs completed:", actual_epochs)

loss, accuracy = ann_model.evaluate(
    X_test,
    y_test,
    verbose=0
)

probability = ann_model.predict(
    X_test,
    verbose=0
)

probability = np.asarray(probability).reshape(-1)
y_pred = (probability >= 0.5).astype(np.int32)

ann_accuracy = accuracy_score(y_test, y_pred)

print(
    "\nANN Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print(
    "Accuracy Score:",
    round(ann_accuracy * 100, 2),
    "%"
)

print(
    "\nFinal Training Accuracy:",
    round(history.history["accuracy"][-1] * 100, 2),
    "%"
)

print(
    "Final Validation Accuracy:",
    round(history.history["val_accuracy"][-1] * 100, 2),
    "%"
)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Purples")
plt.title("ANN Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 5))
plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
plt.title("ANN Training and Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 5))
plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")
plt.title("ANN Training and Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.tight_layout()
plt.show()

with open(ANN_SCALER_FILE, "wb") as file:
    pickle.dump(ann_scaler, file)

ann_model.save(ANN_FILE)

print("ANN model saved.")
print("\nSaving movie information...")

prepared.to_pickle(MOVIES_FILE)

print("Movie data saved.")

with open(KNN_FILE, "rb") as file:
    test_knn = pickle.load(file)

with open(SCALER_FILE, "rb") as file:
    test_scaler = pickle.load(file)

test_movies = pd.read_pickle(MOVIES_FILE)

if len(test_movies) != len(prepared):
    raise ValueError("Saved movies count does not match training data.")

test_vector = np.asarray(
    test_movies.loc[0, "features"],
    dtype=np.float64
)

print("\nSaved feature vector shape:", test_vector.shape)

test_vector = test_vector.reshape(1, -1)

print("KNN test input shape:", test_vector.shape)

if test_vector.ndim != 2:
    raise ValueError("KNN test vector is not 2D.")

if test_vector.shape[1] != 7:
    raise ValueError(
        "KNN test vector must contain exactly 7 features."
    )

test_distances, test_indices = test_knn.kneighbors(
    test_vector,
    n_neighbors=min(2, len(test_movies))
)