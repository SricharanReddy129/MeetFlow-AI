"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchMeetings, deleteMeetingById } from "../../services/meetingApi";

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

  async function handleDelete(id: string) {
    const token = await getToken();
    if (!token) return;
    await deleteMeetingById(token, id);
    setMeetings((prev) => prev.filter((m) => m.id !== id));
  }

  if (loading) {
    return <div style={{ padding: "40px" }}>Loading...</div>;
  }

  return (
    <div style={{ padding: "40px", maxWidth: "700px" }}>
      <h1>Meeting History</h1>

      {meetings.length === 0 && <p>No meetings yet.</p>}

      {meetings.map((meeting) => (
        <div
          key={meeting.id}
          style={{ border: "1px solid #ccc", padding: "15px", marginBottom: "10px" }}
        >
          <h3>{meeting.title}</h3>
          <p style={{ color: "#666", fontSize: "0.9em" }}>
            {new Date(meeting.created_at).toLocaleString()} — {meeting.transcript_word_count} words
          </p>
          <button onClick={() => handleView(meeting)}>View</button>
          <button
            style={{ marginLeft: "10px" }}
            onClick={() => handleDelete(meeting.id)}
          >
            Delete
          </button>
        </div>
      ))}

      <Link href="/dashboard">Back to Dashboard</Link>
    </div>
  );
}