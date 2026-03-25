import { type HTMLAttributes } from "react";

export function Card({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`rounded-shell border border-line bg-paper/90 p-6 shadow-soft backdrop-blur ${className}`}
      {...props}
    />
  );
}
