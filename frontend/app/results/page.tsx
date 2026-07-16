"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";
import { downloadMeetingPdf } from "../../services/meetingApi";

interface MeetingResult {
  id: string;
  title: string;
  summary: string;
  action_items: string[];
  transcript_word_count: number;
  created_at: string;
}

export default function ResultsPage() {
  const { getToken } = useAuth();
  const [result, setResult] = useState<MeetingResult | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("meetingResult");
    if (stored) {
      setResult(JSON.parse(stored));
    }
  }, []);

  async function handleDownload() {
    if (!result) return;
    const token = await getToken();
    if (!token) return;
    await downloadMeetingPdf(token, result.id, result.title);
  }

  if (!result) {
    return (
      <main className="page-shell">
        <div className="page-frame">
          <div className="empty-state">
            <p>No results to show.</p>
            <Link className="subtle-link" href="/history">
              Back to History
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="page-shell">
      <div className="page-frame">
        <section className="page-card result-card">
          <div className="page-hero">
            <div>
              <div className="page-kicker">Result</div>
              <h1 className="page-title">{result.title}</h1>
              <p className="result-meta">{result.transcript_word_count} words</p>
            </div>
            <div className="button-row">
              <button className="primary-button" onClick={handleDownload}>
                Download PDF
              </button>
              <Link className="button-link secondary-button" href="/history">
                Back to History
              </Link>
            </div>
          </div>

          <div className="result-list">
            <section className="summary-card">
              <div className="page-kicker">Summary</div>
              <p className="result-summary">{result.summary}</p>
            </section>

            <section className="summary-card">
              <div className="page-kicker">Action Items</div>
              <ul className="action-list">
                {result.action_items.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}