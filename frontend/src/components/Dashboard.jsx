import { useState } from "react";

import ApiStatus from "./ApiStatus";
import StatCard from "./StatCard";
import GDPChart from "./GDPChart";
import RiskGauge from "./RiskGauge";
import InputCard from "./InputCard";
import ResultCard from "./ResultCard";
import ModelBadge from "./ModelBadge";
import HistoryTable from "./HistoryTable";


import { predictEconomy } from "../api";

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [history, setHistory] = useState([]);

  async function handlePredict(inputs) {
    try {
      setLoading(true);

      const response = await predictEconomy(inputs);

      setResult(response);

      setChartData(prev => [
        ...prev,
        {
          year: inputs.year,
          gdp: inputs.gdp / 1e9,
        },
      ]);

      setHistory(prev => [
        {
          year: inputs.year,
          ...response,
        },
        ...prev,
      ]);
    } catch (err) {
      console.error(err);
      alert("Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="w-full max-w-6xl p-8 space-y-10">

      <h1 className="text-4xl font-bold text-center">
        🌍 Economic Forecast Dashboard
      </h1>

      <div className="flex justify-center">
        <ModelBadge />
      </div>

      <ApiStatus />

      <div className="grid md:grid-cols-3 gap-6">
        <StatCard title="Country" value="Pakistan" />
        <StatCard title="Model Status" value="Live" />
        <StatCard title="Last Update" value="Real-Time" />
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <InputCard onPredict={handlePredict} loading={loading} />
        <ResultCard result={result} />
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        <GDPChart data={chartData} />
        <RiskGauge risk={result?.economic_risk} />
      </div>

      <HistoryTable history={history} />

    </div>
  );
}
