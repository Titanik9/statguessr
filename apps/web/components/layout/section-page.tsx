import { Card } from "@/components/ui/card";

type Row = Record<string, string>;

type SectionPageProps = {
  eyebrow: string;
  title: string;
  description: string;
  rows: Row[];
};

export function SectionPage({ eyebrow, title, description, rows }: SectionPageProps) {
  const headers = rows[0] ? Object.keys(rows[0]) : [];

  return (
    <div className="space-y-6">
      <div>
        <div className="text-xs uppercase tracking-[0.18em] text-muted">{eyebrow}</div>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-ink">{title}</h1>
        <p className="mt-3 max-w-3xl text-sm leading-7 text-muted">{description}</p>
      </div>
      <Card className="overflow-hidden p-0">
        <div className="grid grid-cols-1 divide-y divide-line">
          <div className="grid gap-4 px-6 py-4 text-xs uppercase tracking-[0.16em] text-muted md:grid-cols-4">
            {headers.map((header) => (
              <div key={header}>{header}</div>
            ))}
          </div>
          {rows.map((row, index) => (
            <div key={index} className="grid gap-4 px-6 py-5 text-sm text-ink md:grid-cols-4">
              {headers.map((header) => (
                <div key={header}>{row[header]}</div>
              ))}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
