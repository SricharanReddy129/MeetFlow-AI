import { UserButton } from "@clerk/nextjs";
import { getUserDashboardData } from "../../services/api";
import UpgradeButton from "../../components/UpgradeButton";
import NewMeetingUpload from "../../components/NewMeetingUpload";
import Link from "next/link";

export default async function Dashboard() {
  const data = await getUserDashboardData();

  if (!data) return <div>Error loading dashboard data.</div>;

  return (
    <div style={{ padding: "40px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
        }}
      >
        <h1 style={{ margin: 0 }}>Welcome, {data.name}</h1>
        <UserButton />
      </div>

      <p>Current Plan: <strong>{data.plan}</strong></p>

      {data.plan === "FREE" && (
        <div style={{ border: "1px solid #ccc", padding: "20px", marginTop: "20px" }}>
          <h3>Usage Status</h3>
          <p>Daily Usage: {data.daily_usage}</p>
          <p>Attempts Left: {data.remaining_attempts}</p>
          <UpgradeButton />
        </div>
      )}

      <NewMeetingUpload />

      <Link href="/history">
        <button style={{ marginTop: "20px" }}>View History</button>
      </Link>
    </div>
  );
}