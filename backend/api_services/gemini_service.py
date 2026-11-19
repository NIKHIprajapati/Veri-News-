import os
import json
# pyrefly: ignore[missing-import]
from google import genai  # type: ignore # pyrefly: ignore[missing-import]

def analyze_with_gemini(article_text, article_title=""):
    """
    Analyzes a news article or headline using Gemini AI.
    Returns structured fact-checking insight, credibility score, and claim breakdown.
    Gracefully handles missing API keys or errors without breaking the app.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        return {
            "available": False,
            "status": "key_missing",
            "verdict": "API Key Required",
            "credibility_score": None,
            "summary": "Gemini API key is not yet set in backend/.env. Add your free key to unlock real-time AI fact-checking.",
            "key_claims": [],
            "red_flags": [],
            "sensationalism_level": "Unknown"
        }

    try:
        prompt = f"""
You are an expert news fact-checker and media literacy analyst.
Analyze the following news article / text for truthfulness, accuracy, logic, and factual credibility.

Title: {article_title if article_title else "N/A"}
Article Text:
{article_text[:6000]}

Respond ONLY in valid, parseable JSON with this exact schema:
{{
  "verdict": "Likely Real" | "Likely Fake" | "Unverified / Misleading",
  "credibility_score": <number between 0 and 100>,
  "summary": "<2-3 sentence clear explanation of the factual accuracy and reasoning>",
  "key_claims": [
    {{
      "claim": "<statement made>",
      "status": "Verified True" | "Misleading" | "False / Debunked" | "Unsubstantiated",
      "detail": "<brief context on this claim>"
    }}
  ],
  "sensationalism_level": "Low" | "Medium" | "High",
  "red_flags": [
    "<any warning sign found, e.g. lack of primary source, emotionally loaded language, clickbait headline, etc.>"
  ]
}}
"""

        client = genai.Client(api_key=api_key)
        
        # Candidate model names in priority order
        models_to_try = [
            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-3.8-flash"
        ]

        text_response = ""
        last_error = None

        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    text_response = response.text
                    break
            except Exception as ex:
                last_error = ex
                continue

        if not text_response:
            raise Exception(f"All Gemini models failed. Last error: {str(last_error)}")

        # Extract JSON from response
        clean_json_str = text_response.strip()
        if clean_json_str.startswith("```json"):
            clean_json_str = clean_json_str[7:]
        elif clean_json_str.startswith("```"):
            clean_json_str = clean_json_str[3:]
        if clean_json_str.endswith("```"):
            clean_json_str = clean_json_str[:-3]
        clean_json_str = clean_json_str.strip()

        parsed = json.loads(clean_json_str)
        parsed["available"] = True
        parsed["status"] = "success"
        return parsed

    except Exception as e:
        print("Gemini fact-check error:", str(e))
        return {
            "available": False,
            "status": "error",
            "verdict": "AI Analysis Unavailable",
            "credibility_score": None,
            "summary": f"Could not complete AI verification: {str(e)}",
            "key_claims": [],
            "red_flags": [],
            "sensationalism_level": "Unknown"
        }
