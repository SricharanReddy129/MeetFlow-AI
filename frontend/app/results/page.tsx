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
      <div style={{ padding: "40px" }}>
        <p>No results to show.</p>
        <Link href="/history">Back to History</Link>
      </div>
    );
  }

  return (
    <div style={{ padding: "40px", maxWidth: "700px" }}>
      <h1>{result.title}</h1>
      <p style={{ color: "#666" }}>{result.transcript_word_count} words</p>

      <h3>Summary</h3>
      <p>{result.summary}</p>

      <h3>Action Items</h3>
      <ul>
        {result.action_items.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>

      <button onClick={handleDownload}>Download PDF</button>
      <div style={{ marginTop: "10px" }}>
        <Link href="/history">Back to History</Link>
      </div>
    </div>
  );
}