import { useState } from "react";

export default function InputCard({ onPredict, loading }) {
  const [form, setForm] = useState({
    country: "PAK",
    year: 2024,
    gdp: "",
    inflation: "",
    unemployment: "",
  });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function submit() {
    onPredict({
      country: form.country,
      year: Number(form.year),
      gdp: Number(form.gdp),
      inflation: Number(form.inflation),
      unemployment: Number(form.unemployment),
    });
  }

  return (
    <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl p-8 shadow-2xl">
      <h2 className="text-2xl font-semibold mb-6">Economic Inputs</h2>

      <div className="space-y-5">
        {["country", "year", "gdp", "inflation", "unemployment"].map((key) => (
          <input
            key={key}
            name={key}
            value={form[key]}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-xl bg-black/40 border border-white/20 focus:outline-none focus:ring-2 focus:ring-red-500"
            placeholder={key.toUpperCase()}
          />
        ))}

        <button
          onClick={submit}
          disabled={loading}
          className="w-full mt-6 py-4 rounded-full bg-red-600 hover:bg-red-700 transition-all duration-300 text-lg font-semibold shadow-xl disabled:opacity-50"
        >
          {loading ? "Predicting..." : "Predict Economy"}
        </button>
      </div>
    </div>
  );
}
