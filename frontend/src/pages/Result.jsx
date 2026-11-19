import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import "../assets/styles/Result.css";

function Result() {
  const location = useLocation();
  const navigate = useNavigate();

  const newsText = location.state?.newsText || "";
  const newsUrl = location.state?.newsUrl || "";

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const analyzeNews = async () => {
      if (!newsText && !newsUrl) {
        setError("No news article or URL was submitted.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError("");

        const response = await fetch("http://127.0.0.1:5000/api/predict", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: newsText,
            url: newsUrl,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Failed to analyze the news.");
        }

        setResult(data);
      } catch (err) {
        console.error("Analysis error:", err);
        setError(
          err.message || "Something went wrong while analyzing the news."
        );
      } finally {
        setLoading(false);
      }
    };

    analyzeNews();
  }, [newsText, newsUrl]);

  const getResultClass = (prediction) => {
    if (!prediction) return "";

    const value = prediction.toLowerCase();

    if (value.includes("real")) {
      return "result-real";
    }

    if (value.includes("fake")) {
      return "result-fake";
    }

    return "result-manual";
  };

  const getResultMessage = (prediction) => {
    if (!prediction) {
      return "Unable to determine the result.";
    }

    const value = prediction.toLowerCase();

    if (value.includes("real")) {
      return "The machine learning model classified this news as likely real.";
    }

    if (value.includes("fake")) {
      return "The machine learning model classified this news as likely fake.";
    }

    return "The available evidence is not strong enough for a confident classification.";
  };

  if (loading) {
    return (
      <>
        <nav className="navbar">
          <div className="container navbar-container">
            <div className="logo-section">
              <img
                src="/logo.png"
                alt="VeriNews Logo"
                className="logo"
              />

              <div>
                <h2 className="logo-title">VeriNews</h2>
                <p className="logo-subtitle">
                  News Verification Platform
                </p>
              </div>
            </div>

            <div className="nav-links">
              <Link to="/">Home</Link>
              <Link to="/about">About</Link>
            </div>
          </div>
        </nav>

        <main className="result-page">
          <div className="container">
            <div className="loading-card">
              <h2>Analyzing News...</h2>
              <p>
                VeriNews is analyzing the submitted news article.
                Please wait.
              </p>

              <div className="loading-spinner"></div>
            </div>
          </div>
        </main>
      </>
    );
  }

  if (error) {
    return (
      <>
        <nav className="navbar">
          <div className="container navbar-container">
            <div className="logo-section">
              <img
                src="/logo.png"
                alt="VeriNews Logo"
                className="logo"
              />

              <div>
                <h2 className="logo-title">VeriNews</h2>
                <p className="logo-subtitle">
                  News Verification Platform
                </p>
              </div>
            </div>

            <div className="nav-links">
              <Link to="/">Home</Link>
              <Link to="/about">About</Link>
            </div>
          </div>
        </nav>

        <main className="result-page">
          <div className="container">
            <div className="error-card">
              <h2>Analysis Failed</h2>
              <p>{error}</p>

              <button
                className="primary-btn"
                onClick={() => navigate("/")}
              >
                Go Back
              </button>
            </div>
          </div>
        </main>
      </>
    );
  }

  const prediction = result?.prediction || "Unknown";

  const confidence =
    result?.confidence !== undefined
      ? Number(result.confidence).toFixed(2)
      : "0.00";

  const sources = Array.isArray(result?.sources)
    ? result.sources
    : [];

  const sourceCount =
    result?.sourceCount !== undefined
      ? result.sourceCount
      : sources.length;

  return (
    <>
      {/* Navbar */}
      <nav className="navbar">
        <div className="container navbar-container">
          <div className="logo-section">
            <img
              src="/logo.png"
              alt="VeriNews Logo"
              className="logo"
            />

            <div>
              <h2 className="logo-title">VeriNews</h2>
              <p className="logo-subtitle">
                News Verification Platform
              </p>
            </div>
          </div>

          <div className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>
          </div>
        </div>
      </nav>

      {/* Result Page */}
      <main className="result-page">
        <div className="container">

          {/* Page Heading */}
          <section className="result-header">
            <h1>News Verification Result</h1>

            <p>
              VeriNews analyzed the submitted news using its
              machine learning model and available news sources.
            </p>
          </section>

          {/* Main Result */}
          <section className="result-card">

            <div className="result-card-header">
              <h2>Verification Result</h2>
            </div>

            <div className={`result-status ${getResultClass(prediction)}`}>
              <h1>{prediction}</h1>

              <p>{getResultMessage(prediction)}</p>
            </div>

            <div className="result-stats">

              <div className="stat-box">
                <h3>Machine Learning Confidence</h3>

                <strong>{confidence}%</strong>
              </div>

              <div className="stat-box">
                <h3>Sources Found</h3>

                <strong>{sourceCount}</strong>
              </div>

            </div>
          </section>

          {/* Submitted News */}
          <section className="result-section">

            <h2>Submitted News</h2>

            {newsText && (
              <div className="submitted-content">
                <h3>News Article</h3>

                <p>{newsText}</p>
              </div>
            )}

            {newsUrl && (
              <div className="submitted-content">
                <h3>News URL</h3>

                <a
                  href={newsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="submitted-url"
                >
                  {newsUrl}
                </a>
              </div>
            )}

          </section>

          {/* Machine Learning Prediction */}
          <section className="result-section">

            <h2>Machine Learning Prediction</h2>

            <div className="prediction-box">

              <div>
                <span className="prediction-label">
                  Prediction
                </span>

                <strong className={getResultClass(prediction)}>
                  {prediction}
                </strong>
              </div>

              <div>
                <span className="prediction-label">
                  Confidence
                </span>

                <strong>{confidence}%</strong>
              </div>

            </div>

          </section>

          {/* Matching Sources */}
          <section className="result-section">

            <div className="section-heading-row">
              <div>
                <h2>Source Verification</h2>

                <p>
                  News sources related to the submitted article
                  were found during source discovery.
                </p>
              </div>

              <div className="source-count">
                {sourceCount} Sources
              </div>
            </div>

            {sources.length > 0 ? (
              <div className="sources-list">

                {sources.map((source, index) => (
                  <div
                    className="source-card"
                    key={`${source.url || "source"}-${index}`}
                  >

                    <div className="source-number">
                      {index + 1}
                    </div>

                    <div className="source-content">

                      <h3>
                        {source.title || "News Article"}
                      </h3>

                      <p className="source-publisher">
                        <strong>Publisher:</strong>{" "}
                        {source.publisher || "Unknown"}
                      </p>

                      {source.publishedAt && (
                        <p className="source-date">
                          <strong>Published:</strong>{" "}
                          {source.publishedAt}
                        </p>
                      )}

                      {source.url && (
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-link"
                        >
                          Read Article →
                        </a>
                      )}

                    </div>

                  </div>
                ))}

              </div>
            ) : (
              <div className="no-sources">
                <h3>No Matching Sources Found</h3>

                <p>
                  VeriNews could not find related news sources
                  for this submission.
                </p>
              </div>
            )}

          </section>

          {/* Fact Check Placeholder */}
          <section className="result-section">

            <h2>Fact Check Information</h2>

            <div className="fact-check-box">

              <h3>Fact Check Database</h3>

              <p>
                Fact-check database verification will be added
                in the next stage of VeriNews.
              </p>

              <span className="coming-soon">
                Coming Soon
              </span>

            </div>

          </section>

          {/* Important Note */}
          <section className="result-note">

            <h3>Important Note</h3>

            <p>
              The machine learning prediction is an automated
              assessment and should not be considered absolute
              proof that a news article is true or false.
              VeriNews will combine additional fact-checking
              evidence and source information in future stages
              to improve verification accuracy.
            </p>

          </section>

          {/* Back Button */}
          <div className="result-actions">

            <button
              className="primary-btn"
              onClick={() => navigate("/")}
            >
              Analyze Another News
            </button>

          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container">

          <h2>VeriNews</h2>

          <p>
            © 2026 VeriNews. All Rights Reserved.
          </p>

          <p>Developed by</p>

          <h3>
            Vansh Patel &amp; Dhruvil Patel
          </h3>

          <p>GSFC University</p>

          <p>
            Bachelor of Technology (Computer Science &amp;
            Engineering)
          </p>

        </div>
      </footer>
    </>
  );
}

export default Result;