export default function ModelBadge() {
  return (
    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full
                    bg-white/10 border border-white/20 backdrop-blur-lg
                    text-sm font-medium shadow-lg">
      <span className="w-2 h-2 rounded-full bg-green-400"></span>
      Model v1.0 • World Bank Data
    </div>
  );
}
