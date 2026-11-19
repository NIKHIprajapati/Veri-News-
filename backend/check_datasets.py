import pandas as pd
import os

print("\n========== WELFAKE DATASET ==========\n")

welfake_path = "datasets/welfake/WELFake_Dataset.csv"

if os.path.exists(welfake_path):
    welfake = pd.read_csv(welfake_path)

    print("File found:", welfake_path)
    print("Rows:", len(welfake))
    print("Columns:", list(welfake.columns))

    print("\nFirst 5 records:")
    print(welfake.head())

    print("\nLabel distribution:")
    print(welfake["label"].value_counts())

else:
    print("WELFake file NOT FOUND:")
    print(welfake_path)


print("\n========== LIAR DATASET ==========\n")

liar_files = [
    "train.tsv",
    "valid.tsv",
    "test.tsv"
]

for file in liar_files:

    path = os.path.join("datasets/liar", file)

    if os.path.exists(path):

        data = pd.read_csv(
            path,
            sep="\t",
            header=None
        )

        print(f"\n{file}")
        print("-" * 40)
        print("Rows:", len(data))
        print("Columns:", len(data.columns))

        print("\nFirst 3 records:")
        print(data.head(3))

        print("\nLabels:")
        print(data[1].value_counts())

    else:
        print(f"\n{file} NOT FOUND")


print("\n========== CHECK COMPLETE ==========\n")