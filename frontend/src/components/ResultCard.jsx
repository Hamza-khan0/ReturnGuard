export default function ResultCard({ result }) {
  if (!result) {
    return (
      <div className="backdrop-blur-xl bg-white/5 border border-white/20 rounded-3xl p-8 shadow-2xl">
        <h2 className="text-2xl font-semibold mb-6">Prediction Output</h2>
        <p className="text-gray-400">Awaiting prediction…</p>
      </div>
    );
  }

  return (
    <div className="backdrop-blur-xl bg-white/5 border border-white/20 rounded-3xl p-8 shadow-2xl">
      <h2 className="text-2xl font-semibold mb-6">Prediction Output</h2>

      <div className="space-y-6 text-lg">
        <div>
          <span className="font-medium">Economic Risk:</span>{" "}
          {result.economic_risk ? "High" : "Low"}
        </div>
        <div>
          <span className="font-medium">GDP Growth (Next Year):</span>{" "}
          {result.predicted_gdp_growth_next_year}%
        </div>
        <div>
          <span className="font-medium">Economic Cluster:</span>{" "}
          {result.economic_cluster}
        </div>
      </div>
    </div>
  );
}
