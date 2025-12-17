import { useEffect, useState } from "react";

export default function ApiStatus() {
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then(() => setStatus("online"))
      .catch(() => setStatus("offline"));
  }, []);

  const color =
    status === "online"
      ? "bg-green-500"
      : status === "offline"
      ? "bg-red-500"
      : "bg-yellow-400";

  return (
    <div className="flex items-center justify-center gap-3">
      <span className={`w-3 h-3 rounded-full ${color}`} />
      <span className="text-sm uppercase tracking-wide">
        API Status: {status}
      </span>
    </div>
  );
}
