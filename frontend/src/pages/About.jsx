const OBJECTIVES = [
  "Detect whether a news article is likely real or fake.",
  "Analyze both pasted articles and news URLs.",
  "Show a credibility score.",
  "Provide supporting evidence from trusted news sources.",
];
const TECH = ["React (Frontend)", "FastAPI (Backend)", "MongoDB", "HTML5", "CSS3", "Python"];
const APIS = ["Google Fact Check API", "NewsAPI", "GNews API", "NewsData.io API", "Hugging Face Model"];
const FEATURES = [
  "Multi-source verification",
  "Detailed explanation",
  "Related articles",
  "Source information",
  "Credibility score",
  "Professional report",
];
const TEAM = ["Vansh Patel", "Dhruvil Patel"];
const STEPS = [
  ["You submit an article or URL", "Paste the text or enter a link to the story."],
  ["Machine learning prediction", "A pre-trained model estimates whether the writing looks real or fake."],
  ["Fact-check database search", "We look for claims already reviewed by fact-checkers."],
  ["Related article search", "We find how other news sources cover the same topic."],
  ["Credibility score calculation", "All signals are combined into one score out of 100."],
  ["Verification report", "You get the score, the explanation and the sources."],
];

function List({ title, items }) {
  return (
    <div>
      <h3>{title}</h3>
      <ul className="plain-list">
        {items.map((i) => (
          <li key={i}>{i}</li>
        ))}
      </ul>
    </div>
  );
}

export default function About() {
  return (
    <>
      <section className="about-hero">
        <div className="container">
          <h1>About VeriNews</h1>
          <p>
            VeriNews is a web-based news verification platform that helps people judge the credibility of online
            articles. Instead of relying on a single source, it checks news against multiple trusted APIs,
            fact-check databases and a pre-trained machine learning model, then presents a detailed verification report.
          </p>
        </div>
      </section>

      <div className="container">
        <section className="about-section">
          <h2>How verification works</h2>
          <ol className="steps">
            {STEPS.map(([title, desc]) => (
              <li key={title}>
                <strong>{title}</strong>
                <span>{desc}</span>
              </li>
            ))}
          </ol>
        </section>

        <section className="about-section">
          <div className="about-cols">
            <List title="Project objectives" items={OBJECTIVES} />
            <List title="Key features" items={FEATURES} />
            <List title="Project team" items={TEAM} />
          </div>
        </section>

        <section className="about-section">
          <div className="about-cols">
            <div>
              <h3>Technologies used</h3>
              <ul className="chips">
                {TECH.map((t) => (
                  <li className="chip" key={t}>{t}</li>
                ))}
              </ul>
            </div>
            <div style={{ gridColumn: "span 2" }}>
              <h3>APIs used</h3>
              <ul className="chips">
                {APIS.map((t) => (
                  <li className="chip" key={t}>{t}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}