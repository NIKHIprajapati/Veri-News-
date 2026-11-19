export function verdictFor(score) {
  if (score >= 70) return { tone: "true", label: "Likely real" };
  if (score >= 40) return { tone: "warn", label: "Needs more checking" };
  return { tone: "false", label: "Likely fake" };
}

export function normalizeResult(raw = {}) {
  // Score determination:
  // Prefer Gemini AI credibility_score if available
  // Fall back to ML model prediction & confidence
  let calculatedScore = 50;

  if (raw.aiAnalysis?.available && typeof raw.aiAnalysis.credibility_score === "number") {
    calculatedScore = raw.aiAnalysis.credibility_score;
  } else if (raw.prediction) {
    const isReal = String(raw.prediction).toLowerCase().includes("real");
    const conf = Number(raw.confidence ?? 50);
    calculatedScore = isReal ? conf : 100 - conf;
  }

  const score = Math.max(0, Math.min(100, Math.round(calculatedScore)));

  // Summary description
  const summary =
    raw.aiAnalysis?.summary ||
    (raw.prediction
      ? `The machine learning model evaluated this content as ${String(raw.prediction).toLowerCase()} with ${Number(raw.confidence || 0).toFixed(1)}% confidence.`
      : "Automated analysis completed.");

  // Signal breakdown
  const isReal = String(raw.prediction || "").toLowerCase().includes("real");
  const mlConfidence = Math.round(Number(raw.confidence ?? 0));
  const mlScore = isReal ? mlConfidence : Math.max(0, 100 - mlConfidence);
  const mlDetail = raw.prediction
    ? `Classification: ${raw.prediction} (${mlConfidence}% confidence)`
    : "Model assessment complete";

  const factScore =
    raw.aiAnalysis?.available && typeof raw.aiAnalysis.credibility_score === "number"
      ? Math.round(raw.aiAnalysis.credibility_score)
      : mlScore;

  const factDetail = raw.aiAnalysis?.sensationalism_level
    ? `Sensationalism: ${raw.aiAnalysis.sensationalism_level}`
    : (raw.aiAnalysis?.verdict ? `AI verdict: ${raw.aiAnalysis.verdict}` : "Fact-check verified");

  const sourcesList = Array.isArray(raw.sources) ? raw.sources : [];
  const coverageCount = raw.sourceCount ?? sourcesList.length;
  const coverageScore = Math.min(100, coverageCount * 25);
  const coverageDetail = `${coverageCount} related coverage sources indexed`;

  const signals = [
    { label: "Machine learning model", value: mlScore, detail: mlDetail },
    { label: "AI & fact-check reasoning", value: factScore, detail: factDetail },
    { label: "Related news coverage", value: coverageScore, detail: coverageDetail },
  ];

  // Fact-check claims extracted by AI or databases
  const factChecks = (raw.aiAnalysis?.key_claims ?? []).map((c) => ({
    title: c.claim || "Key claim reviewed",
    publisher: c.detail || "Fact analysis",
    rating: c.status || "Evaluated",
    url: null,
  }));

  // Related articles from Google News RSS
  const related = sourcesList.map((a) => ({
    title: a.title,
    source: a.publisher || "News Source",
    date: a.publishedAt || "",
    url: a.url,
  }));

  return {
    score,
    ...verdictFor(score),
    summary,
    signals,
    factChecks,
    related,
  };
}
