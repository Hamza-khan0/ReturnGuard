export default function RiskGauge({ risk }) {
  const label =
    risk === 1 ? "High Risk" : "Low Risk";

  const color =
    risk === 1 ? "text-red-500" : "text-green-500";

  return (
    <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 shadow-xl flex flex-col items-center justify-center">
      <h2 className="text-xl font-semibold mb-4">
        Economic Risk
      </h2>
      <div className={`text-5xl font-bold ${color}`}>
        {label}
      </div>
    </div>
  );
}
