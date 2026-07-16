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