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