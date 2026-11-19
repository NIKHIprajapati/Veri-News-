import pandas as pd
import joblib
import os

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# Paths
# ==========================================

MODEL_FILE = "models/fake_news_model.pkl"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"

LIAR_TRAIN = "datasets/liar/train.tsv"
LIAR_VALIDATION = "datasets/liar/valid.tsv"
LIAR_TEST = "datasets/liar/test.tsv"


# ==========================================
# Load Model and Vectorizer
# ==========================================

print("\n==========================================")
print("Loading WELFake trained model...")
print("==========================================")

if not os.path.exists(MODEL_FILE):
    print("ERROR: Trained model not found.")
    print(MODEL_FILE)
    exit()

if not os.path.exists(VECTORIZER_FILE):
    print("ERROR: TF-IDF vectorizer not found.")
    print(VECTORIZER_FILE)
    exit()


model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

print("Model loaded successfully.")
print("Vectorizer loaded successfully.")


# ==========================================
# LIAR Label Conversion
# ==========================================

def convert_label(label):

    real_labels = [
        "true",
        "mostly-true",
        "half-true"
    ]

    fake_labels = [
        "barely-true",
        "false",
        "pants-fire"
    ]

    if label in real_labels:
        return 1

    if label in fake_labels:
        return 0

    return None


# ==========================================
# Load LIAR Dataset
# ==========================================

def load_liar_file(file_path):

    print("\nLoading:", file_path)

    if not os.path.exists(file_path):
        print("ERROR: File not found.")
        return None

    df = pd.read_csv(
        file_path,
        sep="\t",
        header=None
    )

    print("Original rows:", len(df))

    # LIAR format:
    # Column 0 = ID
    # Column 1 = Label
    # Column 2 = Statement

    df = df[[1, 2]]

    df.columns = [
        "label",
        "statement"
    ]

    # Convert labels
    df["converted_label"] = df["label"].apply(
        convert_label
    )

    # Remove unsupported labels
    df = df.dropna(
        subset=[
            "statement",
            "converted_label"
        ]
    )

    # Convert label to integer
    df["converted_label"] = df[
        "converted_label"
    ].astype(int)

    # Convert statement to string
    df["statement"] = df[
        "statement"
    ].astype(str)

    print(
        "Rows after label conversion:",
        len(df)
    )

    return df


# ==========================================
# Evaluate One Dataset
# ==========================================

def evaluate_dataset(df, dataset_name):

    print("\n==========================================")
    print(dataset_name)
    print("==========================================")

    X = df["statement"]
    y = df["converted_label"]

    print("Samples:", len(df))

    print("\nActual label distribution:")
    print(y.value_counts())

    # Convert text to TF-IDF
    X_tfidf = vectorizer.transform(X)

    # Prediction
    predictions = model.predict(X_tfidf)

    # Accuracy
    accuracy = accuracy_score(
        y,
        predictions
    )

    print(
        f"\nAccuracy: {accuracy * 100:.2f}%"
    )

    # Classification report
    print("\nClassification Report:")

    print(
        classification_report(
            y,
            predictions,
            labels=[0, 1],
            target_names=[
                "Fake",
                "Real"
            ],
            zero_division=0
        )
    )

    # Confusion matrix
    matrix = confusion_matrix(
        y,
        predictions,
        labels=[0, 1]
    )

    print("Confusion Matrix:")

    print(matrix)

    return accuracy


# ==========================================
# Load LIAR Files
# ==========================================

train_df = load_liar_file(
    LIAR_TRAIN
)

validation_df = load_liar_file(
    LIAR_VALIDATION
)

test_df = load_liar_file(
    LIAR_TEST
)


# ==========================================
# Evaluate LIAR Test Dataset
# ==========================================

if test_df is not None:

    test_accuracy = evaluate_dataset(
        test_df,
        "LIAR TEST DATASET"
    )

else:

    test_accuracy = None


# ==========================================
# Evaluate LIAR Validation Dataset
# ==========================================

if validation_df is not None:

    validation_accuracy = evaluate_dataset(
        validation_df,
        "LIAR VALIDATION DATASET"
    )

else:

    validation_accuracy = None


# ==========================================
# Final Result
# ==========================================

print("\n==========================================")
print("LIAR EVALUATION COMPLETE")
print("==========================================")

if test_accuracy is not None:

    print(
        f"LIAR Test Accuracy: "
        f"{test_accuracy * 100:.2f}%"
    )

if validation_accuracy is not None:

    print(
        f"LIAR Validation Accuracy: "
        f"{validation_accuracy * 100:.2f}%"
    )

print("\nThe WELFake-trained model was")
print("evaluated on the separate LIAR dataset.")

print("\n==========================================")