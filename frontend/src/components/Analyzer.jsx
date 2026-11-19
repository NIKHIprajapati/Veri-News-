import { useEffect, useState } from "react";

const MIN_CHARS = 80;
const STAGES = [
  "Reading the article",
  "Running the credibility model",
  "Searching fact-check databases",
  "Finding related coverage",
];

function isValidUrl(value) {
  try {
    const u = new URL(value);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

export default function Analyzer({ onAnalyze, loading, serverError }) {
  const [mode, setMode] = useState("text"); // "text" | "url"
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [error, setError] = useState("");
  const [stage, setStage] = useState(0);

  useEffect(() => {
    if (!loading) return;
    const id = setInterval(() => setStage((s) => (s + 1) % STAGES.length), 2500);
    return () => clearInterval(id);
  }, [loading]);

  function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setStage(0);

    if (mode === "text") {
      const value = text.trim();
      if (!value) return setError("Paste the article text to check it.");
      if (value.length < MIN_CHARS)
        return setError(`Paste more of the article. At least ${MIN_CHARS} characters gives a reliable result.`);
      onAnalyze({ type: "text", value });
    } else {
      const value = url.trim();
      if (!value) return setError("Enter the link to the news article.");
      if (!isValidUrl(value))
        return setError("That link doesn't look right. Start it with http:// or https://");
      onAnalyze({ type: "url", value });
    }
  }

  const shownError = error || serverError;

  return (
    <section className="analyzer" aria-labelledby="analyzer-title">
      <h2 id="analyzer-title" className="sr-only">Check a news story</h2>

      <div className="tabs" role="tablist" aria-label="Input type">
        <button
          type="button"
          role="tab"
          className="tab"
          id="tab-text"
          aria-selected={mode === "text"}
          aria-controls="panel-main"
          onClick={() => { setMode("text"); setError(""); }}
        >
          Paste article
        </button>
        <button
          type="button"
          role="tab"
          className="tab"
          id="tab-url"
          aria-selected={mode === "url"}
          aria-controls="panel-main"
          onClick={() => { setMode("url"); setError(""); }}
        >
          Enter link
        </button>
      </div>

      <form className="analyzer__body" id="panel-main" role="tabpanel" onSubmit={handleSubmit} noValidate>
        {mode === "text" ? (
          <>
            <label htmlFor="article-text" className="field-label">News article</label>
            <p className="hint">Paste the full article for the most accurate result.</p>
            <textarea
              id="article-text"
              className="input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste the complete news article here"
              aria-invalid={Boolean(shownError)}
            />
          </>
        ) : (
          <>
            <label htmlFor="article-url" className="field-label">Article link</label>
            <p className="hint">We read the article from the page and check it.</p>
            <input
              id="article-url"
              type="url"
              className="input"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/news/article"
              aria-invalid={Boolean(shownError)}
            />
          </>
        )}

        {shownError && <div className="error" role="alert">{shownError}</div>}

        <div className="analyzer__foot">
          <span className="counter" aria-live="off">
            {mode === "text" ? `${text.trim().length} characters` : "Public news pages only"}
          </span>
          <div className="analyzer__actions">
            {(text || url) && !loading && (
              <button
                type="button"
                className="btn-text-clear"
                onClick={() => {
                  setText("");
                  setUrl("");
                  setError("");
                }}
              >
                Clear
              </button>
            )}
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading && <span className="spinner" aria-hidden="true" />}
              {loading ? "Checking" : "Check this news"}
            </button>
          </div>
        </div>

        {loading && <p className="status" role="status" aria-live="polite">{STAGES[stage]}…</p>}
      </form>
    </section>
  );
}
