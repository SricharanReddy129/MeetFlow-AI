"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { uploadMeeting } from "../services/meetingApi";

export default function NewMeetingUpload() {
  const { getToken } = useAuth();
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload() {
    if (!file) {
      setError("Please choose a file first.");
      return;
    }

    setLoading(true);
    setError(null);

    const token = await getToken();
    if (!token) {
      setError("Please log in again.");
      setLoading(false);
      return;
    }

    const result = await uploadMeeting(token, file);

    if (result.ok) {
      sessionStorage.setItem("meetingResult", JSON.stringify(result.data));
      router.push("/results");
    } else {
      const detail = result.data?.detail || "Something went wrong. Please try again.";
      setError(detail);
    }

    setLoading(false);
  }

  return (
    <div className="upload-content">
      <div className="upload-field">
        <input
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button className="primary-button" onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload & Summarize"}
        </button>
      </div>
      {error && <p className="upload-error">{error}</p>}
    </div>
  );
}