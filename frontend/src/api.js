const API_BASE = "https://returnguard-backend.onrender.com";

export async function predictEconomy(inputs) {
  const res = await fetch(`${API_BASE}/predict/economy`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputs),
  });

  if (!res.ok) throw new Error("Prediction failed");
  return res.json();
}
