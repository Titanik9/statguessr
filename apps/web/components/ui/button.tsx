import { type ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  tone?: "primary" | "secondary" | "ghost";
};

export function Button({ className = "", tone = "primary", ...props }: ButtonProps) {
  const tones = {
    primary: "bg-emerald text-white shadow-soft hover:opacity-95",
    secondary: "bg-paper text-ink border border-line hover:bg-white",
    ghost: "bg-transparent text-ink hover:bg-white/60",
  } as const;

  return (
    <button
      className={`inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-medium transition ${tones[tone]} ${className}`}
      {...props}
    />
  );
}
