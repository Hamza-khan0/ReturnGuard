export default function StatCard({ title, value }) {
  return (
    <div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl p-6 shadow-xl text-center">
      <p className="text-sm uppercase tracking-wide text-gray-300">
        {title}
      </p>
      <p className="text-2xl font-bold mt-2">
        {value}
      </p>
    </div>
  );
}
