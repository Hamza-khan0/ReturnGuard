import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div style={{ maxWidth: 300, margin: "100px auto", textAlign: "center" }}>
      <h2>ReturnGuard</h2>
      <input placeholder="Email" style={{ width: "100%", padding: 10 }} />
      <br /><br />
      <input type="password" placeholder="Password" style={{ width: "100%", padding: 10 }} />
      <br /><br />
      <button onClick={() => navigate("/dashboard")} style={{ width: "100%", padding: 10 }}>
        Login
      </button>
    </div>
  );
}
