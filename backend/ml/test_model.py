import joblib
import os


# ==========================================
# Model Paths
# ==========================================

MODEL_FILE = "models/fake_news_model.pkl"
VECTORIZER_FILE = "models/tfidf_vectorizer.pkl"


# ==========================================
# Check Model Files
# ==========================================

if not os.path.exists(MODEL_FILE):
    print("ERROR: Model file not found.")
    print(MODEL_FILE)
    exit()

if not os.path.exists(VECTORIZER_FILE):
    print("ERROR: Vectorizer file not found.")
    print(VECTORIZER_FILE)
    exit()


# ==========================================
# Load Model
# ==========================================

print("\nLoading trained model...")

model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

print("Model loaded successfully.")


# ==========================================
# Prediction Function
# ==========================================

def predict_news(news_text):

    # Convert text into TF-IDF
    text_vector = vectorizer.transform(
        [news_text]
    )

    # Prediction
    prediction = model.predict(
        text_vector
    )[0]

    # Probability
    probabilities = model.predict_proba(
        text_vector
    )[0]

    confidence = max(probabilities) * 100

    # Label (WELFake: 0 = Real, 1 = Fake)
    if prediction == 0:
        label = "LIKELY REAL"
    else:
        label = "LIKELY FAKE"

    return label, confidence


# ==========================================
# Interactive Testing
# ==========================================

print("\n==========================================")
print("VeriNews AI Model Tester")
print("==========================================")

print("\nEnter a news statement to analyze.")

print("Type 'exit' to stop.")


while True:

    print("\n------------------------------------------")

    news = input("Enter news: ")

    if news.lower() == "exit":
        print("\nExiting model tester...")
        break

    if not news.strip():
        print("Please enter some news text.")
        continue

    label, confidence = predict_news(
        news
    )

    print("\nPrediction:", label)
    print(
        f"Confidence: {confidence:.2f}%"
    )