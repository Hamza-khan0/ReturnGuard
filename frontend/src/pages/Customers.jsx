import { useEffect, useState } from "react";

export default function Customers() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        visits: 5,
        days_since_last_visit: 25,
        avg_gap: 7,
        total_spend: 1200
      })
    })
      .then(res => res.json())
      .then(result => setData(result))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Customer Prediction</h2>

      {!data ? (
        <p>Loading...</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>Risk</th>
              <th>Predicted Return (Days)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{data.risk}</td>
              <td>{data.predicted_return_days}</td>
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
}
