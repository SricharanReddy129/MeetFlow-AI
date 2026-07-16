"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface MeetingResult {
  id: string;
  title: string;
  summary: string;
  action_items: string[];
  transcript_word_count: number;
  created_at: string;
}

export default function ResultsPage() {
  const [result, setResult] = useState<MeetingResult | null>(null);

  useEffect(() => {
    const stored = sessionStorage.getItem("meetingResult");
    if (stored) {
      setResult(JSON.parse(stored));
    }
  }, []);

  if (!result) {
    return (
      <div style={{ padding: "40px" }}>
        <p>No results to show.</p>
        <Link href="/dashboard">Back to Dashboard</Link>
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

      <Link href="/history">Back to History</Link>
    </div>
  );
}