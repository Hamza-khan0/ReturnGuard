import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div style={{ padding: 20 }}>
      <h2>Dashboard</h2>

      <div style={{ display: "flex", gap: 20 }}>
        <Card title="Total Customers" value="120" />
        <Card title="At Risk" value="18" />
        <Card title="Safe" value="102" />
      </div>

      <br />

      <Link to="/customers">View Customers</Link> |{" "}
      <Link to="/upload">Upload Data</Link>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={{ padding: 20, border: "1px solid #ccc", width: 150 }}>
      <h4>{title}</h4>
      <p>{value}</p>
    </div>
  );
}
