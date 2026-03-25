const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

export async function requestMagicLink(email: string) {
  const response = await fetch(`${apiBase}/auth/magic-links/request`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    const data = (await response.json().catch(() => ({}))) as { detail?: string };
    throw new Error(data.detail ?? "Unable to request magic link.");
  }

  return response.json() as Promise<{ message: string; preview_url?: string | null }>;
}
