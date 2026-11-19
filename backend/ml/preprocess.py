import pandas as pd
import re
import os
from sklearn.model_selection import train_test_split


# ==============================
# Paths
# ==============================

INPUT_FILE = "datasets/welfake/WELFake_Dataset.csv"
OUTPUT_DIR = "datasets/welfake/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================
# Load Dataset
# ==============================

print("\nLoading WELFake dataset...")

df = pd.read_csv(INPUT_FILE)

print("Original rows:", len(df))
print("Original columns:", list(df.columns))


# ==============================
# Keep Required Columns
# ==============================

df = df[["title", "text", "label"]]


# ==============================
# Remove Missing Values
# ==============================

df = df.dropna(subset=["title", "text", "label"])

print("Rows after removing missing values:", len(df))


# ==============================
# Combine Title + Text
# ==============================

df["content"] = df["title"].astype(str) + " " + df["text"].astype(str)


# ==============================
# Clean Text
# ==============================

def clean_text(text):
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


print("Cleaning text...")

df["content"] = df["content"].apply(clean_text)


# ==============================
# Remove Empty Content
# ==============================

df = df[df["content"].str.len() > 0]


# ==============================
# Remove Duplicate Articles
# ==============================

df = df.drop_duplicates(subset=["content"])

print("Rows after cleaning:", len(df))


# ==============================
# Train / Validation / Test Split
# ==============================

print("\nSplitting dataset...")

train_df, temp_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)

validation_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["label"]
)


# ==============================
# Save Processed Datasets
# ==============================

train_df[["content", "label"]].to_csv(
    f"{OUTPUT_DIR}/train.csv",
    index=False
)

validation_df[["content", "label"]].to_csv(
    f"{OUTPUT_DIR}/validation.csv",
    index=False
)

test_df[["content", "label"]].to_csv(
    f"{OUTPUT_DIR}/test.csv",
    index=False
)


# ==============================
# Display Information
# ==============================

print("\n========== PREPROCESSING COMPLETE ==========")

print("Training samples:", len(train_df))
print("Validation samples:", len(validation_df))
print("Testing samples:", len(test_df))

print("\nTraining label distribution:")
print(train_df["label"].value_counts())

print("\nValidation label distribution:")
print(validation_df["label"].value_counts())

print("\nTesting label distribution:")
print(test_df["label"].value_counts())

print("\nFiles created:")

print(f"{OUTPUT_DIR}/train.csv")
print(f"{OUTPUT_DIR}/validation.csv")
print(f"{OUTPUT_DIR}/test.csv")

print("\n============================================")