export default function HistoryTable({ history }) {
  if (!history || history.length === 0) return null;

  return (
    <div className="backdrop-blur-xl bg-white/5 border border-white/20 rounded-3xl p-6 shadow-2xl">
      <h2 className="text-xl font-semibold mb-4">
        Prediction History
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="border-b border-white/20 text-gray-300">
            <tr>
              <th className="py-2">Year</th>
              <th>Risk</th>
              <th>GDP Growth</th>
              <th>Cluster</th>
            </tr>
          </thead>
          <tbody>
            {history.map((row, idx) => (
              <tr
                key={idx}
                className="border-b border-white/10"
              >
                <td className="py-2">{row.year}</td>
                <td
                  className={
                    row.economic_risk
                      ? "text-red-400"
                      : "text-green-400"
                  }
                >
                  {row.economic_risk ? "High" : "Low"}
                </td>
                <td>{row.predicted_gdp_growth_next_year}%</td>
                <td>{row.economic_cluster}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
