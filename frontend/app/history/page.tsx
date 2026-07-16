"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchMeetings, deleteMeetingById, downloadMeetingPdf } from "../../services/meetingApi";

interface Meeting {
  id: string;
  title: string;
  summary: string;
  action_items: string[];
  transcript_word_count: number;
  created_at: string;
}

export default function HistoryPage() {
  const { getToken } = useAuth();
  const router = useRouter();
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [confirmingId, setConfirmingId] = useState<string | null>(null);

  async function loadMeetings() {
    setLoading(true);
    const token = await getToken();
    if (!token) return;
    const data = await fetchMeetings(token);
    setMeetings(Array.isArray(data) ? data : []);
    setLoading(false);
  }

  useEffect(() => {
    loadMeetings();
  }, []);

  async function handleView(meeting: Meeting) {
    sessionStorage.setItem("meetingResult", JSON.stringify(meeting));
    router.push("/results");
  }

  async function handleDownload(meeting: Meeting) {
    const token = await getToken();
    if (!token) return;
    await downloadMeetingPdf(token, meeting.id, meeting.title);
  }

  async function handleConfirmDelete(id: string) {
    const token = await getToken();
    if (!token) return;
    await deleteMeetingById(token, id);
    setMeetings((prev) => prev.filter((m) => m.id !== id));
    setConfirmingId(null);
  }

  if (loading) {
    return (
      <main className="page-shell">
        <div className="page-frame">
          <div className="empty-state">Loading...</div>
        </div>
      </main>
    );
  }

  return (
    <main className="page-shell">
      <div className="page-frame">
        <section className="page-card">
          <div className="page-hero">
            <div>
              <div className="page-kicker">History</div>
              <h1 className="page-title">Meeting history</h1>
              <p className="page-copy">
                Review past summaries, download PDFs, or remove entries you no longer need.
              </p>
            </div>
            <div className="button-row">
              <Link className="button-link secondary-button" href="/dashboard">
                Back to Dashboard
              </Link>
            </div>
          </div>

          {meetings.length === 0 ? (
            <div className="empty-state">No meetings yet.</div>
          ) : (
            <div className="history-list">
              {meetings.map((meeting) => (
                <article key={meeting.id} className="meeting-card">
                  <h3>{meeting.title}</h3>
                  <p className="meeting-meta">
                    {new Date(meeting.created_at).toLocaleString()} — {meeting.transcript_word_count} words
                  </p>

                  <div className="button-row">
                    <button className="primary-button" onClick={() => handleView(meeting)}>
                      View
                    </button>
                    <button className="secondary-button" onClick={() => handleDownload(meeting)}>
                      Download PDF
                    </button>

                    {confirmingId === meeting.id ? (
                      <>
                        <span className="upload-note">Delete this meeting?</span>
                        <button className="destructive-button" onClick={() => handleConfirmDelete(meeting.id)}>
                          Confirm
                        </button>
                        <button className="ghost-button" onClick={() => setConfirmingId(null)}>
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button className="ghost-button" onClick={() => setConfirmingId(meeting.id)}>
                        Delete
                      </button>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}