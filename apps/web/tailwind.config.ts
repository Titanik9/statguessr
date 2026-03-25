import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: "var(--canvas)",
        ink: "var(--ink)",
        muted: "var(--muted)",
        line: "var(--line)",
        emerald: "var(--emerald)",
        ember: "var(--ember)",
        paper: "var(--paper)",
      },
      boxShadow: {
        soft: "0 18px 45px rgba(20, 25, 23, 0.08)",
      },
      borderRadius: {
        shell: "1.5rem",
      },
    },
  },
  plugins: [],
};

export default config;
