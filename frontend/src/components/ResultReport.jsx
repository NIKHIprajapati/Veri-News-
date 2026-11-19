import { forwardRef, useEffect, useState } from "react";

function Gauge({ score }) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    const id = requestAnimationFrame(() => setShown(score));
    return () => cancelAnimationFrame(id);
  }, [score]);

  return (
    <svg className="gauge" viewBox="0 0 200 120" role="img" aria-label={`Credibility score ${score} out of 100`}>
      <path className="gauge__track" d="M 15 100 A 85 85 0 0 1 185 100" pathLength="100" />
      <path
        className="gauge__value"
        d="M 15 100 A 85 85 0 0 1 185 100"
        pathLength="100"
        strokeDasharray="100"
        strokeDashoffset={100 - shown}
      />
      <text className="gauge__score" x="100" y="92">{score}</text>
      <text className="gauge__label" x="100" y="112">credibility score out of 100</text>
    </svg>
  );
}

function formatDate(value) {
  if (!value) return "";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

const ResultReport = forwardRef(function ResultReport({ result, onReset }, ref) {
  if (!result) return null;
  const { score, tone, label, summary, signals, factChecks, related } = result;

  return (
    <div className="report" ref={ref} tabIndex={-1} aria-live="polite">
      {onReset && (
        <div className="report-header-nav">
          <button type="button" className="btn-back" onClick={onReset} id="btn-back-top">
            ← Check Another Story
          </button>
        </div>
      )}
      <section className="verdict" data-tone={tone} aria-labelledby="verdict-label">
        <Gauge score={score} />
        <div>
          <h2 className="verdict__label" id="verdict-label">{label}</h2>
          {summary && <p className="verdict__summary">{summary}</p>}
          <p className="verdict__note">
            This is an automated estimate based on the sources below, not a final ruling. Check the linked sources before you share.
          </p>
        </div>
      </section>

      <section className="report-section">
        <h3>How we got this score</h3>
        <p>Each check contributes to the overall credibility score.</p>
        <ul className="signal-list">
          {signals.map((s) => (
            <li className="signal" key={s.label}>
              <div className="signal__head">
                <span>{s.label}</span>
                <span>{Math.round(s.value)}%</span>
              </div>
              <div className="signal__bar">
                <span style={{ width: `${Math.max(0, Math.min(100, s.value))}%` }} />
              </div>
              {s.detail && <p className="signal__detail">{s.detail}</p>}
            </li>
          ))}
        </ul>
      </section>

      <section className="report-section">
        <h3>Fact-check results</h3>
        <p>Claims reviewed by fact-checking and media analysis intelligence.</p>
        {factChecks && factChecks.length ? (
          <ul className="evidence-list">
            {factChecks.map((f, i) => (
              <li className="evidence" key={i}>
                {f.url ? (
                  <a className="evidence__title" href={f.url} target="_blank" rel="noopener noreferrer">
                    {f.title}
                  </a>
                ) : (
                  <span className="evidence__text">{f.title}</span>
                )}
                {f.rating && <span className="rating">{f.rating}</span>}
                <p className="evidence__meta">{f.publisher}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty">No fact-checks were found for this story. That does not mean it is true or false.</p>
        )}
      </section>

      <section className="report-section">
        <h3>Related coverage</h3>
        <p>What other news sources are reporting on this topic.</p>
        {related && related.length ? (
          <ul className="evidence-list">
            {related.map((a, i) => (
              <li className="evidence" key={i}>
                <a className="evidence__title" href={a.url} target="_blank" rel="noopener noreferrer">
                  {a.title}
                </a>
                <p className="evidence__meta">{[a.source, formatDate(a.date)].filter(Boolean).join(" · ")}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="empty">No related articles were found from the connected news sources.</p>
        )}
      </section>

      {onReset && (
        <div className="report-bottom-actions">
          <button type="button" className="btn-primary" onClick={onReset} id="btn-back-bottom">
            ← Verify Another News Article
          </button>
        </div>
      )}
    </div>
  );
});

export default ResultReport;
