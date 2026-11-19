from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import joblib
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv

import trafilatura

from api_services.gemini_service import analyze_with_gemini

# Load environment variables (.env)
load_dotenv()

app = Flask(__name__)
CORS(app)


# ============================================================
# MODEL PATHS (Robust Absolute Paths)
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fake_news_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")



# ============================================================
# LOAD ML MODEL
# ============================================================

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    print("ML model loaded successfully.")
    print("TF-IDF vectorizer loaded successfully.")

except Exception as e:
    model = None
    vectorizer = None

    print("ERROR loading ML model:")
    print(e)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# NORMALIZE TEXT FOR RELEVANCE CHECKING

STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "to",
    "of",
    "and",
    "or",
    "in",
    "on",
    "for",
    "with",
    "at",
    "by",
    "from",
    "as",
    "that",
    "this",
    "it",
    "its",
    "into",
    "about",
    "after",
    "before",
    "during",
    "than",
    "then",
    "has",
    "have",
    "had",
    "will",
    "would",
    "can",
    "could",
    "should",
    "may",
    "might",
    "do",
    "does",
    "did",
    "not",
    "but",
    "if",
    "they",
    "their",
    "them",
    "he",
    "she",
    "his",
    "her",
    "we",
    "our",
    "you",
    "your",
    "i",
    "me",
    "my"
}


def tokenize(text):
    text = clean_text(text).lower()

    words = re.findall(r"[a-zA-Z0-9]+", text)

    return {
        word
        for word in words
        if len(word) >= 3 and word not in STOP_WORDS
    }


# CREATE SEARCH QUERIES

def create_search_queries(text, title=""):
    """
    Creates several smaller and more useful search queries.

    Instead of sending the entire article to Google News,
    we use the title and important words from the article.
    """

    text = clean_text(text)
    title = clean_text(title)

    queries = []

    # 1. Title query

    if title:
        title_words = title.split()

        if len(title_words) > 14:
            title_query = " ".join(title_words[:14])
        else:
            title_query = title

        if title_query:
            queries.append(title_query)

    # --------------------------------------------------------
    # 2. First important part of article
    # --------------------------------------------------------

    important_words = [
        word
        for word in re.findall(r"[A-Za-z0-9]+", text)
        if len(word) >= 4 and word.lower() not in STOP_WORDS
    ]

    if important_words:

        unique_words = []

        for word in important_words:
            lower_word = word.lower()

            if lower_word not in {
                item.lower() for item in unique_words
            }:
                unique_words.append(word)

            if len(unique_words) >= 10:
                break

        if unique_words:
            queries.append(" ".join(unique_words))

    # --------------------------------------------------------
    # Remove duplicate queries
    # --------------------------------------------------------

    final_queries = []

    for query in queries:
        query = query.strip()

        if query and query.lower() not in [
            q.lower() for q in final_queries
        ]:
            final_queries.append(query)

    return final_queries[:2]


# ============================================================
# FETCH ARTICLE FROM URL
# ============================================================

def fetch_article_from_url(url):

    if not url:
        return {
            "success": False,
            "title": "",
            "text": "",
            "error": "No URL provided."
        }

    try:

        parsed = urllib.parse.urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            return {
                "success": False,
                "title": "",
                "text": "",
                "error": "URL must start with http:// or https://"
            }

        print()
        print("Fetching article URL:")
        print(url)

        downloaded = trafilatura.fetch_url(url)

        if not downloaded:
            return {
                "success": False,
                "title": "",
                "text": "",
                "error": "Could not download the webpage."
            }

        # Extract main article text
        extracted_text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            include_links=False,
            favor_precision=True
        )

        # Extract metadata
        metadata = trafilatura.extract_metadata(downloaded)

        title = ""

        if metadata and metadata.title:
            title = metadata.title

        extracted_text = clean_text(extracted_text)

        if not extracted_text:
            return {
                "success": False,
                "title": title,
                "text": "",
                "error": "Could not extract readable article content from this URL."
            }

        print("Article title:")
        print(title)

        print("Extracted article characters:")
        print(len(extracted_text))

        return {
            "success": True,
            "title": title,
            "text": extracted_text,
            "error": ""
        }

    except Exception as e:

        print("URL extraction error:")
        print(e)

        return {
            "success": False,
            "title": "",
            "text": "",
            "error": str(e)
        }


# ============================================================
# GOOGLE NEWS RSS SEARCH
# ============================================================

def search_google_news_rss(query):

    try:

        encoded_query = urllib.parse.quote(query)

        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_query}"
            "&hl=en-IN"
            "&gl=IN"
            "&ceid=IN:en"
        )

        print()
        print("Google News search:")
        print(query)

        request = urllib.request.Request(
            rss_url,
            headers={
                "User-Agent": (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = response.read()

        root = ET.fromstring(data)

        results = []

        for item in root.findall(".//item"):

            title_element = item.find("title")
            link_element = item.find("link")
            date_element = item.find("pubDate")
            source_element = item.find("source")

            title = (
                title_element.text.strip()
                if title_element is not None and title_element.text
                else ""
            )

            url = (
                link_element.text.strip()
                if link_element is not None and link_element.text
                else ""
            )

            published_at = (
                date_element.text.strip()
                if date_element is not None and date_element.text
                else ""
            )

            publisher = (
                source_element.text.strip()
                if source_element is not None and source_element.text
                else ""
            )

            if title and url:

                results.append({
                    "title": title,
                    "publisher": publisher,
                    "url": url,
                    "publishedAt": published_at
                })

        return results

    except Exception as e:

        print("Google News RSS error:")
        print(e)

        return []


# ============================================================
# RELEVANCE SCORE
# ============================================================

def calculate_relevance_score(query, article_title, article_text=""):

    query_tokens = tokenize(query)
    title_tokens = tokenize(article_title)

    if not query_tokens or not title_tokens:
        return 0.0

    # --------------------------------------------------------
    # Title overlap
    # --------------------------------------------------------

    common_title_words = query_tokens.intersection(title_tokens)

    title_overlap = (
        len(common_title_words) / len(query_tokens)
    ) if query_tokens else 0

    # --------------------------------------------------------
    # Important word matching
    # --------------------------------------------------------

    text_tokens = tokenize(article_text)

    common_text_words = query_tokens.intersection(text_tokens)

    text_overlap = (
        len(common_text_words) / len(query_tokens)
    ) if query_tokens else 0

    # --------------------------------------------------------
    # Weighted score
    #
    # Title is more important than generic article text.
    # --------------------------------------------------------

    score = (
        (title_overlap * 0.75)
        +
        (text_overlap * 0.25)
    )

    return round(score * 100, 2)


# ============================================================
# FIND RELEVANT NEWS SOURCES
# ============================================================

def find_relevant_sources(article_text, article_title=""):

    queries = create_search_queries(
        article_text,
        article_title
    )

    print()
    print("Generated search queries:")
    for query in queries:
        print("-", query)

    all_sources = []

    # --------------------------------------------------------
    # Search using each query
    # --------------------------------------------------------

    for query in queries:

        search_results = search_google_news_rss(query)

        for source in search_results:

            relevance = calculate_relevance_score(
                query,
                source["title"],
                source["title"]
            )

            source["relevanceScore"] = relevance

            all_sources.append(source)

    # --------------------------------------------------------
    # Remove duplicate URLs
    # --------------------------------------------------------

    unique_sources = {}

    for source in all_sources:

        url = source.get("url", "").strip()

        if not url:
            continue

        if url not in unique_sources:
            unique_sources[url] = source

        else:

            # Keep the higher relevance score
            old_score = unique_sources[url].get(
                "relevanceScore",
                0
            )

            new_score = source.get(
                "relevanceScore",
                0
            )

            if new_score > old_score:
                unique_sources[url] = source

    sources = list(unique_sources.values())

    # --------------------------------------------------------
    # Sort by relevance
    # --------------------------------------------------------

    sources.sort(
        key=lambda item: item.get(
            "relevanceScore",
            0
        ),
        reverse=True
    )

    # --------------------------------------------------------
    # Only keep genuinely relevant sources
    #
    # 50% is our minimum relevance threshold.
    # --------------------------------------------------------

    relevant_sources = [
        source
        for source in sources
        if source.get("relevanceScore", 0) >= 50
    ]

    # --------------------------------------------------------
    # Maximum 8 sources
    #
    # IMPORTANT:
    # 8 is now a MAXIMUM, NOT a guaranteed number.
    # --------------------------------------------------------

    relevant_sources = relevant_sources[:8]

    print()
    print("Relevant sources found:")
    print(len(relevant_sources))

    for source in relevant_sources:

        print(
            f"{source['relevanceScore']}% - "
            f"{source['title']}"
        )

    return relevant_sources


# ============================================================
# ML PREDICTION
# ============================================================

def predict_news(text):

    if not model or not vectorizer:
        raise Exception(
            "ML model or vectorizer is not loaded."
        )

    cleaned = clean_text(text)

    if not cleaned:
        raise Exception(
            "No article text available for prediction."
        )

    transformed = vectorizer.transform(
        [cleaned]
    )

    prediction = model.predict(
        transformed
    )[0]

    probabilities = model.predict_proba(
        transformed
    )[0]

    confidence = float(
        max(probabilities) * 100
    )

    # WELFake Dataset Mapping:
    # 0 = Real News (e.g. verified news wire articles)
    # 1 = Fake News (fabricated / misleading articles)
    if int(prediction) == 0:
        label = "Likely Real"
    else:
        label = "Likely Fake"

    return {
        "prediction": label,
        "confidence": round(confidence, 2)
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "VeriNews backend is running."
    })


@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "ok",
        "modelLoaded": model is not None,
        "vectorizerLoaded": vectorizer is not None
    })


# ============================================================
# MAIN PREDICTION API
# ============================================================

@app.route("/api/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No request data received."
            }), 400

        submitted_text = (
            data.get("text") or ""
        ).strip()

        submitted_url = (
            data.get("url") or ""
        ).strip()

        # ====================================================
        # ARTICLE CONTENT
        # ====================================================

        article_text = submitted_text
        article_title = ""

        url_extraction = {
            "success": False,
            "title": "",
            "text": "",
            "error": ""
        }

        # ----------------------------------------------------
        # If URL is provided and text is empty:
        # actually fetch and extract the article.
        # ----------------------------------------------------

        if submitted_url and not submitted_text:

            url_extraction = fetch_article_from_url(
                submitted_url
            )

            if not url_extraction["success"]:

                return jsonify({
                    "error": (
                        "Could not analyze the submitted URL. "
                        + url_extraction["error"]
                    )
                }), 400

            article_text = url_extraction["text"]
            article_title = url_extraction["title"]

        # ----------------------------------------------------
        # If both text and URL are provided:
        # text takes priority for ML analysis.
        # ----------------------------------------------------

        elif submitted_text:

            article_text = submitted_text

        # ----------------------------------------------------
        # Nothing submitted
        # ----------------------------------------------------

        if not article_text:

            return jsonify({
                "error": (
                    "Please provide a news article "
                    "or a valid news URL."
                )
            }), 400

        # ====================================================
        # MACHINE LEARNING
        # ====================================================

        ml_result = predict_news(
            article_text
        )

        # ====================================================
        # SOURCE DISCOVERY
        # ====================================================

        sources = find_relevant_sources(
            article_text,
            article_title
        )

        # ====================================================
        # GEMINI 1.5 FLASH FACT-CHECKING & CLAIM ANALYSIS
        # ====================================================

        ai_analysis = analyze_with_gemini(
            article_text,
            article_title
        )

        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        return jsonify({

            "prediction": ml_result["prediction"],

            "confidence": ml_result["confidence"],

            "aiAnalysis": ai_analysis,

            "sources": sources,

            "sourceCount": len(sources),

            "articleTitle": article_title,

            "analyzedText": article_text,

            "urlAnalyzed": bool(
                submitted_url and not submitted_text
            ),

            "urlExtractionSuccess": (
                url_extraction["success"]
            ),

            "message": (
                "News analysis completed successfully."
            )
        })

    except Exception as e:

        print()
        print("Prediction error:")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# RUN SERVER

if __name__ == "__main__":
    import logging
    import flask.cli

    # Silence the development server warning banner
    flask.cli.show_server_banner = lambda *args: None
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print()
    print("==========================================")
    print("        VeriNews Backend Starting")
    print("==========================================")
    print("Backend URL: http://127.0.0.1:5000")
    print("API Status: Ready for verification requests")
    print("==========================================")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=True
    )