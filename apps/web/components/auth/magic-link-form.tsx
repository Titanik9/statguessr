"use client";

import { useState } from "react";

import { requestMagicLink } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function MagicLinkForm() {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setMessage(null);
    setPreviewUrl(null);

    try {
      const data = await requestMagicLink(email);
      setMessage(data.message);
      setPreviewUrl(data.preview_url ?? null);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Unable to request magic link.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <Input
        type="email"
        required
        placeholder="team@your-company.com"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <Button className="w-full" disabled={busy} type="submit">
        {busy ? "Sending link..." : "Send magic link"}
      </Button>
      {message ? <p className="text-sm text-muted">{message}</p> : null}
      {previewUrl ? (
        <a className="block rounded-2xl border border-dashed border-line bg-canvas px-4 py-3 text-sm text-ink" href={previewUrl}>
          Open preview link
        </a>
      ) : null}
    </form>
  );
}
