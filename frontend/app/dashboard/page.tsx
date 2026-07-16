import { UserButton } from "@clerk/nextjs";
import { getUserDashboardData } from "../../services/api";
import UpgradeButton from "../../components/UpgradeButton";
import NewMeetingUpload from "../../components/NewMeetingUpload";
import Link from "next/link";

export default async function Dashboard() {
  const data = await getUserDashboardData();

  if (!data) {
    return (
      <main className="page-shell">
        <div className="page-frame">
          <div className="empty-state">Error loading dashboard data.</div>
        </div>
      </main>
    );
  }

  return (
    <main className="page-shell">
      <div className="page-frame dashboard-layout">
        <section className="dashboard-main">
          <div className="page-card">
            <div className="page-kicker">Dashboard</div>
            <div className="page-hero">
              <div>
                <h1 className="page-title">Welcome, {data.name}</h1>
                <p className="page-copy">
                  Capture meetings, turn them into clear summaries, and keep momentum moving without noise.
                </p>
              </div>
              <UserButton />
            </div>

            <div className="dashboard-stats">
              <div className="stat-card">
                <p className="stat-label">Current plan</p>
                <div className="stat-value">{data.plan}</div>
              </div>
              <div className="stat-card">
                <p className="stat-label">Daily usage</p>
                <div className="stat-value">{data.daily_usage}</div>
              </div>
              <div className="stat-card">
                <p className="stat-label">Attempts left</p>
                <div className="stat-value">{data.remaining_attempts}</div>
              </div>
            </div>
          </div>

          <section className="page-card upload-shell">
            <div className="page-kicker">New Meeting</div>
            <h2 className="panel-title">Upload and summarize</h2>
            <p className="upload-note">
              Drop in a PDF, text, or DOCX file and let MeetFlow build the summary for you.
            </p>
            <NewMeetingUpload />
          </section>
        </section>

        <aside className="dashboard-side">
          {data.plan === "FREE" && (
            <section className="section-card">
              <div className="page-kicker">Usage</div>
              <h2 className="panel-title">Plan status</h2>
              <p className="upload-note">
                You are currently on the free plan. Upgrade to unlock more uploads and a smoother workflow.
              </p>
              <UpgradeButton />
            </section>
          )}

          <section className="section-card">
            <div className="page-kicker">Quick Links</div>
            <h2 className="panel-title">Next step</h2>
            <div className="button-row">
              <Link className="button-link primary-button" href="/history">
                View History
              </Link>
            </div>
          </section>
        </aside>
      </div>
    </main>
  );
}