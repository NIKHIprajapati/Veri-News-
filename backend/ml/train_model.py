import pandas as pd
import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# Paths
# ==========================================

TRAIN_FILE = "datasets/welfake/processed/train.csv"
VALIDATION_FILE = "datasets/welfake/processed/validation.csv"
TEST_FILE = "datasets/welfake/processed/test.csv"

MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# Load Datasets
# ==========================================

print("\n==========================================")
print("Loading processed datasets...")
print("==========================================")

train_df = pd.read_csv(TRAIN_FILE)
validation_df = pd.read_csv(VALIDATION_FILE)
test_df = pd.read_csv(TEST_FILE)

print("Training samples:", len(train_df))
print("Validation samples:", len(validation_df))
print("Testing samples:", len(test_df))


# ==========================================
# Separate Features and Labels
# ==========================================

X_train = train_df["content"]
y_train = train_df["label"]

X_validation = validation_df["content"]
y_validation = validation_df["label"]

X_test = test_df["content"]
y_test = test_df["label"]


# ==========================================
# TF-IDF Vectorization
# ==========================================

print("\n==========================================")
print("Creating TF-IDF vectors...")
print("==========================================")

vectorizer = TfidfVectorizer(
    max_features=100000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)

X_validation_tfidf = vectorizer.transform(X_validation)

X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF vocabulary size:", len(vectorizer.vocabulary_))

print("Training matrix shape:", X_train_tfidf.shape)
print("Validation matrix shape:", X_validation_tfidf.shape)
print("Testing matrix shape:", X_test_tfidf.shape)


# ==========================================
# Train Logistic Regression Model
# ==========================================

print("\n==========================================")
print("Training Logistic Regression model...")
print("==========================================")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)

print("Model training completed.")


# ==========================================
# Validation Evaluation
# ==========================================

print("\n==========================================")
print("Validation Results")
print("==========================================")

validation_predictions = model.predict(X_validation_tfidf)

validation_accuracy = accuracy_score(
    y_validation,
    validation_predictions
)

print(
    f"Validation Accuracy: "
    f"{validation_accuracy * 100:.2f}%"
)


# ==========================================
# Test Evaluation
# ==========================================

print("\n==========================================")
print("Test Results")
print("==========================================")

test_predictions = model.predict(X_test_tfidf)

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

print(
    f"Test Accuracy: "
    f"{test_accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        test_predictions,
        target_names=["Fake", "Real"]
    )
)


# ==========================================
# Save Model
# ==========================================

print("\n==========================================")
print("Saving trained model...")
print("==========================================")

joblib.dump(
    model,
    os.path.join(MODEL_DIR, "fake_news_model.pkl")
)

joblib.dump(
    vectorizer,
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)


# ==========================================
# Save Model Information
# ==========================================

model_info = {
    "model": "Logistic Regression",
    "vectorizer": "TF-IDF",
    "dataset": "WELFake",
    "training_samples": len(train_df),
    "validation_samples": len(validation_df),
    "testing_samples": len(test_df),
    "validation_accuracy": validation_accuracy,
    "test_accuracy": test_accuracy
}

joblib.dump(
    model_info,
    os.path.join(MODEL_DIR, "model_info.pkl")
)


# ==========================================
# Complete
# ==========================================

print("\n==========================================")
print("MODEL TRAINING COMPLETE")
print("==========================================")

print("\nCreated files:")

print("models/fake_news_model.pkl")
print("models/tfidf_vectorizer.pkl")
print("models/model_info.pkl")

print("\n==========================================")