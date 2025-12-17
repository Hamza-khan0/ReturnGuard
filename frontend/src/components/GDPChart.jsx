import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Area,
} from "recharts";

export default function GDPChart({ data = [] }) {
  // build confidence bands
  const enriched = data.map(d => ({
    ...d,
    upper: d.gdp * 1.1,
    lower: d.gdp * 0.9,
  }));

  return (
    <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 shadow-xl">
      <h2 className="text-xl font-semibold mb-4">
        GDP Trend (Billion USD)
      </h2>

      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={enriched}>
          <XAxis dataKey="year" stroke="#ccc" />
          <YAxis stroke="#ccc" />
          <Tooltip />

          {/* Confidence band */}
          <Area
            type="monotone"
            dataKey="upper"
            stroke="none"
            fill="rgba(239,68,68,0.15)"
          />
          <Area
            type="monotone"
            dataKey="lower"
            stroke="none"
            fill="rgba(0,0,0,0)"
          />

          {/* Main GDP line */}
          <Line
            type="monotone"
            dataKey="gdp"
            stroke="#ef4444"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>

      <p className="text-xs text-gray-400 mt-3">
        Shaded area represents ±10% confidence interval
      </p>
    </div>
  );
}
