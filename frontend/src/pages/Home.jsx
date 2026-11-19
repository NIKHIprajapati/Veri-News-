import { useRef, useState } from "react";
import Analyzer from "../components/Analyzer";
import ResultReport from "../components/ResultReport";
import { normalizeResult } from "../utils/normalizeResult";
import { analyzeNews } from "../services/api";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [serverError, setServerError] = useState("");
  const [resetKey, setResetKey] = useState(0);
  const reportRef = useRef(null);
  const analyzerRef = useRef(null);

  async function handleAnalyze(payload) {
    setServerError("");
    setResult(null);
    setLoading(true);
    try {
      const raw = await analyzeNews(payload);
      setResult(normalizeResult(raw));
      setTimeout(() => reportRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 80);
    } catch (err) {
      setServerError(err.message || "We couldn't complete the check. Make sure the server is running, then try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setResult(null);
    setServerError("");
    setResetKey((k) => k + 1);
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }, 40);
  }

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Verify news before you believe it</h1>
          <p>
            Paste an article or a link. VeriNews compares it with fact-check databases and news sources,
            then shows a credibility score with the evidence behind it.
          </p>
        </div>
      </section>

      <div className="container" ref={analyzerRef}>
        <Analyzer key={resetKey} onAnalyze={handleAnalyze} loading={loading} serverError={serverError} />
        <ResultReport result={result} ref={reportRef} onReset={handleReset} />
      </div>

      <section className="sources">
        <div className="container">
          <h2>Where the evidence comes from</h2>
          <p>Every report combines a machine learning prediction with independent sources, so no single source decides the result.</p>
          <ul className="chips">
            {["Machine learning model", "Google Fact Check", "NewsAPI", "GNews", "NewsData.io"].map((s) => (
              <li className="chip" key={s}>{s}</li>
            ))}
          </ul>
        </div>
      </section>
    </>
  );
}