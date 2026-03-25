import type { ReactNode } from "react";

import { Sidebar } from "@/components/layout/sidebar";

export function ConsoleShell({ children }: { children: ReactNode }) {
  return (
    <div className="mx-auto grid min-h-screen max-w-[1600px] gap-6 px-4 py-6 lg:grid-cols-[290px_minmax(0,1fr)] lg:px-6">
      <Sidebar />
      <main className="min-h-[calc(100vh-3rem)] rounded-shell border border-line bg-white/65 p-6 shadow-soft backdrop-blur">
        {children}
      </main>
    </div>
  );
}
