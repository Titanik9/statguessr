import type { ReactNode } from "react";

type BadgeProps = {
  children: ReactNode;
  tone?: "live" | "next" | "muted";
};

export function Badge({ children, tone = "muted" }: BadgeProps) {
  const tones = {
    live: "bg-emerald/10 text-emerald border-emerald/20",
    next: "bg-ember/10 text-ember border-ember/20",
    muted: "bg-white text-muted border-line",
  } as const;

  return <span className={`rounded-full border px-2.5 py-1 text-xs font-medium uppercase tracking-[0.12em] ${tones[tone]}`}>{children}</span>;
}
