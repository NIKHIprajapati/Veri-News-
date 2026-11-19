export async function analyzeNews({ type, value }) {
  const payload = {
    text: type === "text" ? value.trim() : "",
    url: type === "url" ? value.trim() : "",
  };

  const response = await fetch("http://127.0.0.1:5000/api/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || "Failed to analyze the news.");
  }

  return data;
}
