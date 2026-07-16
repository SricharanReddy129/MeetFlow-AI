export async function uploadMeeting(token: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/meetings/new`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  const data = await res.json().catch(() => null);

  return { ok: res.ok, status: res.status, data };
}

export async function fetchMeetings(token: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/meetings`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function fetchMeetingById(token: string, id: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function deleteMeetingById(token: string, id: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function downloadMeetingPdf(token: string, id: string, title: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${id}/pdf`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    throw new Error("Failed to download PDF");
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${title.slice(0, 50).trim().replace(/\s+/g, "_") || "meeting"}.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}