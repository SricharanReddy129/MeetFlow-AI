import { UserButton } from "@clerk/nextjs";
import { getUserDashboardData } from "../../services/api";

export default async function Dashboard() {
  const data = await getUserDashboardData();

  if (!data) return <div>Error loading dashboard data.</div>;

  return (
    <div style={{ padding: "40px" }}>
      <h1>Welcome, {data.name}</h1>
      <p>Current Plan: <strong>{data.plan}</strong></p>

      {/* Conditional UI for FREE users */}
      {data.plan === "FREE" && (
        <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px" }}>
          <h3>Usage Status</h3>
          <p>Daily Usage: {data.daily_usage}</p>
          <p>Attempts Left: {data.remaining_attempts}</p>
          <button style={{ marginTop: "10px" }}>Upgrade to PRO</button>
        </div>
      )}

      {/* History Button (Always visible) */}
      <button style={{ marginTop: "20px" }}>View History</button>
      
      <UserButton />
    </div>
  );
}